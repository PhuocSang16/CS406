# 1. Giới thiệu

Môn: Xử lý ảnh và ứng dụng

Lớp: CS406.O11

Năm học: 2023-2024 

Đồ án: Scenetext detection-recognition system on Vietnamese

Nhóm: KHNT

Thành viên:

|Họ và tên          | MSSV      |
--- | ---
| Đoàn Nhật Sang | 21522542 |
| Trương Văn Khải | 21520274 |
| Lê Ngô Minh Đức | |
| Đặng Phước Sang | |

# 2. Mở đầu 

Chúng tôi cài đặt một e2e method cho bài toán "Scenetext detection-recognition system on Vietnamese" đồng thời xây dựng một web app để demo.

# 3. Cài đặt môi trường

Tạo và kích hoạt conda environment:

```
conda create -n aic2021 python=3.8
conda activate aic2021
```

Tải sourcecode từ github:

```
git clone https://github.com/dnsang1611/aic2021.git
```

Cài đặt requirements:

```
cd parseq
pip install torch==1.10.1+cu111 torchvision==0.11.2+cu111 torchaudio==0.10.1 -f https://download.pytorch.org/whl/cu111/torch_stable.html
pip install -r requirements/parseq.txt -e .[train,test]

cd ../mmocr
pip install -U openmim
mim install mmengine
mim install 'mmcv>==2.0.1'
mim install 'mmdet==3.1.0'
pip install -v -e .

pip install Polygon3 python-Levenshtein==0.12.0
```

# 4. Chuẩn bị dữ liệu

Chúng tôi sử dụng bộ dữ liệu VinText  được cung cấp bởi VinAI. Đầu tiên, hãy tải bộ dữ liệu này trong folder aic2021 theo command sau:

```
gdown 1UUQhNvzgpZy7zXBFQp0Qox-BBjunZ0ml
unzip vietnamese_original.zip
rm vietnamese_original.zip
```

Sẽ có một vài mẫu bị đánh nhãn sai, ta dùng lệnh sau để sửa chúng:

```
python prepare_data/correct_annotations.py
```

## 4.1. DBNetpp

Đổi format giống với yêu cầu của mmocr để train DBNetpp. Sau khi chạy lệnh, ta sẽ thấy xuất hiện 3 files train_instances.json, val_instances.json test_instances.json trong folder vietnamese:

```
python prepare_data/convert2mmocr.py
```

## 4.2. PARSeq

Cắt tất cả bounding boxes trong dataset và lưu trong folder aic2021/vietnamese/recog-data:

```
python prepare_data/crop_image.py
```

Tạo lmdb files, sau khi chạy command, ta sẽ thấy xuất hiện folder aic2021/reocg-data

```
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

cd ..
```

# 5. Train

## 5.1. DBNetpp

Khi train mô hình, checkpoints sẽ được lưu trong folder aic2021/mmocr/workdir:

```
cd mmocr 
CUDA_VISIBLE_DEVICES=0 python tools/train.py './configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py' \
                                             --work-dir './workdir/dbnetpp'
cd ..
```

## 5.2. PARSeq

Khi train mô hình, checkpoints sẽ được lưu trong folder aic2021/parseq/outputs

```
cd parseq
CUDA_VISIBLE_DEVICES=0 python train.py
cd ..
```

# 6. Evaluation

## 6.1. DBNetpp

Tải pretrained DBNetpp trên VinText và đặt vào folder aic2021/pretrained/dbnetpp

```
gdown 1z-H0Kdcb6AZF4h1H6Df46CGxlTRUGr31
```

Kết quả dự đoán của DBNetpp gồm polygons và confidence scores, polygon nào có score càng thấp thể hiện mức độ tự tin của mô hình về dự đoán càng thấp. Vì vậy, ta có thể chọn lọc bỏ những polygons này để đạt được hmean tốt hơn. Ở bước này, ta sẽ gridsearch threshold thuộc [0.1; 0.9] trên tập val để chọn ra threshold cho hmean tốt nhất:

```
CUDA_VISIBLE_DEVICES=0 python tools/test.py \
            configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021_val.py \
            pretrained/dbnetpp/vintext_best_dbnetpp.pth \
            --work-dir gridsearch/val \
            --save-preds
```

Kết quả cho thấy, threshold tốt nhất là 0.7 với recall: 0.8014, precision: 0.9332, hmean: 0.8623 . Ta sử dụng threshold này để đánh giá trên tập test và đạt được recall: 0.8396, precision: 0.9332, hmean: 0.8839.

```
CUDA_VISIBLE_DEVICES=0 python tools/test.py \
            configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py \
            pretrained/dbnetpp/vintext_best_dbnetpp.pth \
            --work-dir gridsearch/val \
            --save-preds
```


## 6.2. PARSeq

Tải pretrained PARSeq trên vintext và đặt tại aic2021/pretrained/parseq:

```
gdown 1qQ-5E1t2YxZzpT8RuNbDKY3Dgb8Ovn7Y
```

Đánh giá:

```
cd parseq
python test_custom.py pretrained/parseq/vintext_best_parseq.ckpt \
                    --data_root ../recog-data
cd ..
```

Kết quả: Accuracy = 0.8703; OneMinusNED = 0.9446

## 6.3. E2E

Chúng tôi sử dụng code đánh giá của AIC2021, code này yêu cầu 2 file zip đầu vào: 1 cho groundtruth, 1 cho kết quả dự đoán. Groundtruth zipfile của tập test đã được VinAI cung cấp sẵn (gt_vintext.zip)

### Gridsearch threshold

Tương tự khi đánh gía riêng DBNetpp, ta vẫn phải chọn ra threshold tốt nhất cho cả pipeline. Do code đánh giá yêu cầu groundtruth zipfile của tập val, nên ta sẽ tiến hành khởi tạo nó:

```
python eval-e2e/tools/generate_val_gt_zip.py
```

Sử dụng pipeline để dự đoán trên tập val:


```
python eval-e2e/tools/infer.py  'vietnamese/test_image' \
                    --out-dir 'eval-e2e/preds-with-score-val' \
                    --det 'mmocr/configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py' \
                    --det-weights 'mmocr/pretrained/dbnetpp/vintext_best_dbnetpp.pth' \
                    --rec-weights 'parseq/pretrained/parseq/vintext_best_parseq.ckpt' 

```

Một folder aic2021/eval-e2e/preds-with-score-val sẽ xuất hiện, mỗi file trong folder có nhiều line, mỗi line có format: x1,y1,x2,y2,x3,y3,x4,y4,det_score,####text.

Tiến hành gridsearch trên [0.1; 0.9]:

```
python eval-e2e/tools/gridsearch_threshold.py \
                    --preds 'eval-e2e/preds-with-score-val' \
                    --pred-zipfile 'eval-e2e/sub' \
                    --gt-zipfile 'eval-e2e/val_gt.zip' \
                    --gs-results 'eval-e2e/val_gs_result.json'
```

Threshold 0.7 cho kết quả tốt nhất với 0.7778, recall: 0.7132, hmean: 0.7441

### Đánh giá trên test

Sử dụng pipeline để dự đoán trên tập test:

```
python eval-e2e/tools/infer.py  'vietnamese/unseen_test_images' \
                    --out-dir 'eval-e2e/preds-with-score-test' \
                    --det 'mmocr/configs/textdet/dbnetpp/dbnetpp_resnet50-dcnv2_fpnc_1200e_aic2021.py' \
                    --det-weights 'mmocr/pretrained/dbnetpp/vintext_best_dbnetpp.pth' \
                    --rec-weights 'parseq/pretrained/parseq/vintext_best_parseq.ckpt' 
```

Đánh giá với threshold = 0.7:

```
python eval-e2e/tools/eval.py \
                    --preds 'eval-e2e/preds-with-score-test' \
                    --pred-zipfile 'eval-e2e/sub' \
                    --gt-zipfile 'eval-e2e/gt_vintext.zip' \
                    --thresh 0.7 
```

Kết quả: precision: 0.8073, recall: 0.7649, hmean: 0.785. So sánh với các phương pháp trong paper "Dictionary-guided Scene Text Recognition", ta có bảng sau:

| Phương pháp | hmean |
| --- | ---|
| ABCNet                            | 54.2 |
| ABCNet + dictionary               | 58.5 |
| ABCNet+D                          | 57.4 |
| ABCNet+D + dictionary             | 63.6 |
| Mask Textspotterv3+D              | 68.5 |
| Mask Textspotterv3+D + dictionary | 70.3 |
| DBNetpp + PARSeq (Ours)           | **78.5** |

# 7. Inference 

Chi tiết xem trong file aic2021/SceneTextPipeline.py

# 8. Demo

Chi tiết xem trong folder frontend/str_app

# 9. Acknowledgements
Minghui Liao cùng đồng nghiệp với DBNetpp. \
Darwin Bautista, Rowel Atienza với PARSeq. \
VinAI với bộ dữ liệu VinText.
