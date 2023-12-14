aic2021_textdet_data_root = '../vietnamese'

aic2021_textdet_train = dict(
    type='OCRDataset',
    data_root=aic2021_textdet_data_root,
    ann_file='train_instances.json',
    data_prefix=dict(img_path='train_images'),
    filter_cfg=dict(filter_empty_gt=True, min_size=32),
    pipeline=None)

aic2021_textdet_val = dict(
    type='OCRDataset',
    data_root=aic2021_textdet_data_root,
    ann_file='val_instances.json',
    data_prefix=dict(img_path='test_image'),
    test_mode=True,
    pipeline=None)

aic2021_textdet_test = dict(
    type='OCRDataset',
    data_root=aic2021_textdet_data_root,
    ann_file='test_instances.json',
    data_prefix=dict(img_path='unseen_test_images'),
    test_mode=True,
    pipeline=None)