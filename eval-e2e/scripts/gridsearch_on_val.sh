# Generate val_gt.zip file
python eval-e2e/tools/generate_val_gt_zip.py

# Infer for val set
python eval-e2e/tools/infer.py  'vietnamese/test_image' \
                    --out-dir 'eval-e2e/preds-with-score-val' \
                    --det 'mmocr/configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py' \
                    --det-weights 'mmocr/pretrained/dbnetpp/vintext_best_dbnetpp.pth' \
                    --rec-weights 'parseq/pretrained/parseq/vintext_best_parseq.ckpt' 

# Gridsearch threshold for e2e method
python eval-e2e/tools/gridsearch_threshold.py \
                    --preds 'eval-e2e/preds-with-score-val' \
                    --pred-zipfile 'eval-e2e/sub' \
                    --gt-zipfile 'eval-e2e/val_gt.zip' \
                    --gs-results 'eval-e2e/val_gs_result.json'