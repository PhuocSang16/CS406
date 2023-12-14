toy_det_data_root = 'tests/data/det_toy_dataset'

toy_det_train = dict(
    type='OCRDataset',
    data_root=toy_det_data_root,
    ann_file='textdet_test.json',
    filter_cfg=dict(filter_empty_gt=True, min_size=32),
    pipeline=None)

toy_det_test = dict(
    type='OCRDataset',
    data_root=toy_det_data_root,
    ann_file='textdet_test.json',
    # data_prefix=dict(img_path='imgs/'),
    test_mode=True,
    pipeline=None)
