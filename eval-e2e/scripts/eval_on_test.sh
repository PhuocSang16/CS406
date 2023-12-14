# # Infer for test set
python eval-e2e/tools/infer.py  'vietnamese/unseen_test_images' \
                    --out-dir 'eval-e2e/preds-with-score-test' \
                    --det 'mmocr/configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py' \
                    --det-weights 'mmocr/pretrained/dbnetpp/vintext_best_dbnetpp.pth' \
                    --rec-weights 'parseq/pretrained/parseq/vintext_best_parseq.ckpt' 
                    
# Evaluate e2e method wiht threshold 0.7
python eval-e2e/tools/eval.py \
                    --preds 'eval-e2e/preds-with-score-test' \
                    --pred-zipfile 'eval-e2e/sub' \
                    --gt-zipfile 'eval-e2e/gt_vintext.zip' \
                    --thresh 0.7 