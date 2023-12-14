import sys
sys.path.append('./')

import cv2
import numpy as np
import os
import shutil
from argparse import ArgumentParser

from SceneTextPipeline import SceneTextPipeline

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        'images', type=str, help='Input image file or folder path.')
    parser.add_argument(
        '--out-dir',
        type=str,
        default='results/',
        help='Output directory of results.')
    parser.add_argument(
        '--det',
        type=str,
        default=None,
        help='config file of detector.')
    parser.add_argument(
        '--det-weights',
        type=str,
        default=None,
        help='Checkpoint of detector.')
    parser.add_argument(
        '--rec-weights',
        type=str,
        default=None,
        help='Checkpoint of recognizer.')

    parser.add_argument(
        '--threshold',
        type=float,
        default=0,
        help='Threshold. Filter out bbboxes with confidence score <= threshold.')
    
    return parser.parse_args()

def main():
    args = parse_args()

    # Renew out folder
    if os.path.isdir(args.out_dir):
        shutil.rmtree(args.out_dir)
    os.mkdir(args.out_dir)

    # Init pipeline
    pipeline = SceneTextPipeline(args.det, args.det_weights, 
                                 args.rec_weights, thresh=args.threshold)

    # Iterate through all images
    inames = sorted(os.listdir(args.images))
    for idx, iname in enumerate(inames):
        ipath = os.path.join(args.images, iname)
        pname = iname.split('.')[0].split('im')[1]
        pname = f'{int(pname):07}.txt'
        ppath = os.path.join(args.out_dir, pname)

        # Open file to write
        wf = open(ppath, 'w', encoding='utf-8')

        img = cv2.imread(ipath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        preds = pipeline([img])[0]
        for polygon, score, text in zip(preds['det_polygons'], preds['det_scores'], preds['texts']):
            wf.write(f'{polygon[0][0]},{polygon[0][1]},{polygon[1][0]},{polygon[1][1]},')
            wf.write(f'{polygon[2][0]},{polygon[2][1]},{polygon[3][0]},{polygon[3][1]},')
            wf.write(f'{round(score, 3)},####{text}\n')

        if (idx + 1) % 100 == 0:
            print(f'{idx + 1}/{len(inames)}')
    
if __name__ == '__main__':
    main()