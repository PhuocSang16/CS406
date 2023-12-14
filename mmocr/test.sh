CUDA_VISIBLE_DEVICES=0 python tools/test.py \
            configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py \
            pretrained/dbnetpp/vintext_best_dbnetpp.pth \
            --work-dir gridsearch/val \
            --save-preds