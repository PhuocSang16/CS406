python test_custom.py outputs/parseq/2023-12-11_19-37-51/checkpoints/epoch=16-step=2193-val_accuracy=86.0536-val_NED=93.7526.ckpt \
            --data_root /mmlabworkspace/Students/visedit/AIC2021/recog-data


python test_custom.py pretrained/parseq/vintext_best_parseq.ckpt \
                    --data_root ../recog-data