# Correct annatations
python prepare_data/correct_annotations.py

# Prepare data for dbnetpp
python prepare_data/convert2mmocr.py

# Prepare data for parseq
python prepare_data/crop_image.py

cd parseq

python tools/create_lmdb_dataset.py '../vietnamese/recog-data' \
                                      '../vietnamese/recog_train_gt.txt' \
                                      '../recog-data/train/sin_hw'

python tools/create_lmdb_dataset.py '../vietnamese/recog-data' \
                                      '../vietnamese/recog_val_gt.txt' \
                                      '../recog-data/val/sin_hw'

python tools/create_lmdb_dataset.py '../vietnamese/recog-data' \
                                      '../vietnamese/recog_test_gt.txt' \
                                      '../recog-data/test/sin_hw'