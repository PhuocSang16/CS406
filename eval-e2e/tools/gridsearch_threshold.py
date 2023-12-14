import text_eval_script
import shutil
import os
import json
from argparse import ArgumentParser

TEMP_FOLDER = 'eval-e2e/preds-filtered'

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--preds', type=str, help='Folder of predictions with scores.')
    parser.add_argument(
        '--pred-zipfile',
        type=str,
        help='Path to prediction zip file.')
    parser.add_argument(
        '--gt-zipfile',
        type=str,
        help='Path to groundtruth zip file.')
    parser.add_argument(
        '--gs-results',
        type=str,
        help='Path to gridsearch results.')
    
    return parser.parse_args()

def main():
    args = parse_args()

    # Gridsearch thresh for e2e
    gs_res = {}
    pnames = sorted(os.listdir(args.preds))

    for thrs in range(1, 10):
        thrs = thrs / 10

        # Renew out folder
        if os.path.isdir(TEMP_FOLDER):
            shutil.rmtree(TEMP_FOLDER)
        os.mkdir(TEMP_FOLDER)
        
        # Iterate through all pred files
        for pname in pnames:
            ppath = os.path.join(args.preds, pname)
            opath = os.path.join(TEMP_FOLDER, pname)
        
            rf = open(ppath, 'r', encoding='utf-8')
            wf = open(opath, 'w', encoding='utf-8')

            for line in rf.readlines():
                spl_line = line.split(',', maxsplit=9)
                polygon = spl_line[:8]
                score = float(spl_line[8])
                text = spl_line[9].split('\n')[0]
                
                if score >= thrs:
                    polygon = ','.join(polygon)
                    wf.write(f'{polygon},{text}\n')

            rf.close()
            wf.close()

        shutil.make_archive(args.pred_zipfile, 'zip', TEMP_FOLDER)
        res_dict = text_eval_script.text_eval_main(args.pred_zipfile + '.zip',
                                    args.gt_zipfile,
                                    True)
        
        gs_res[str(thrs)] = res_dict['e2e_method']

    # Save gridsearch result
    with open(args.gs_results, 'w') as wf:
        json.dump(gs_res, wf, indent=3)

if __name__ == '__main__':
    main()