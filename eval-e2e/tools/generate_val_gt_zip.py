# File gt_vintext.zip coresponds to gt of test
# This file is used to gererate zip file of val to gridsearch threshold for e2e

import os
import shutil

LBL_FOLDER = 'vietnamese/labels'
TEMP_FOLDER = 'eval-e2e/val-gt'
ZIP_FILE = 'eval-e2e/val_gt'

# Create temp folder
os.mkdir(TEMP_FOLDER)

lnames = sorted(os.listdir(LBL_FOLDER))
for lname in lnames:

    img_idx = int(lname.split('gt_')[1].split('.')[0])

    if 1200 < img_idx <= 1500:
        lpath = os.path.join(LBL_FOLDER, lname)
        oname = lname.split('gt_')[1].split('.')[0]
        oname = f'{img_idx:07}.txt'
        opath = os.path.join(TEMP_FOLDER, oname)
        
        wf = open(opath, 'w', encoding='utf-8')

        with open(lpath, 'r', encoding='utf-8') as rf:
            for line in rf.readlines():
                line = line.split(',', maxsplit=8)
                polygon = ','.join(line[:8])
                text = line[8].split('\n')[0]
                wf.write(f'{polygon},####{text}\n')
        
        wf.close()

# Make zip file
shutil.make_archive(ZIP_FILE, 'zip', TEMP_FOLDER)

# Remove temp folder
shutil.rmtree(TEMP_FOLDER)