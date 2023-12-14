# This file is used to convert format to mmocr format 

import json, cv2, os

def convert_format_det(img_folder, out_path):
  data = {
      "metainfo": {
          "dataset_type": "TextDetDataset",
          "task_name": "textdet",
          "category": [
            {
                "id": 0,
                "name": "text"
            }
          ]
        },
      "data_list": []
  }

  print(f'======= {img_folder} ========')

  for idx, img_file in enumerate(sorted(os.listdir(img_folder))):
    img = cv2.imread(os.path.join(img_folder, img_file))
    height, width = img.shape[:2]
    seg_map = f'gt_{int(img_file[2:6])}.txt'
    gt_path = os.path.join('vietnamese/labels', seg_map)
    instances = []

    with open(gt_path, 'r', encoding='utf-8') as rf:
      for line in rf.readlines():
        line = line.split(',')
        polygon = [int(_) for _ in line[:8]]
        text = line[8].strip()
        x_min = max(0, min(polygon[0::2]))
        x_max = min(width, max(polygon[0::2]))
        y_min = max(0, min(polygon[1::2]))
        y_max = min(height, max(polygon[1::2]))
        w = x_max - x_min
        h = y_max - y_min

        instances.append({
            'polygon': polygon,
            'bbox': [x_min, y_min, w, h],
            'bbox_label': 0,
            'ignore': True if text in ('', '###') else False
        })

    data['data_list'].append({
        'instances': instances,
        'img_path': img_file,
        'height': height,
        'width': width,
        'seg_map': seg_map
    })

    if (idx + 1) % 200 == 0:
      print(f'{idx + 1}')

  with open(out_path, 'w') as wf:
    json.dump(data, wf, indent=3)

convert_format_det('vietnamese/train_images', 'vietnamese/train_instances.json')
convert_format_det('vietnamese/test_image', 'vietnamese/val_instances.json')
convert_format_det('vietnamese/unseen_test_images', 'vietnamese/test_instances.json')