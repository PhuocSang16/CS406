python infer_custom.py 'outputs/parseq/2023-12-11_19-37-51/checkpoints/epoch=16-step=2193-val_accuracy=86.0536-val_NED=93.7526.ckpt' \
        --images '../vietnamese/recog-data' \
        --outfile preds.txt \
        --device 'cuda' \
        --batch_size 128