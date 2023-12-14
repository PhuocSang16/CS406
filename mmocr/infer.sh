python tools/infer.py '/mmlabworkspace/Students/visedit/AIC2021/vietnamese/unseen_test_images' \
      --out-dir result \
      --det 'configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py' \
      --det-weight '/mmlabworkspace/Students/visedit/AIC2021/mmocr/pretrained/epoch_600.pth' \
      --device 'cuda' \
      --batch-size 8 \
      --save_pred 