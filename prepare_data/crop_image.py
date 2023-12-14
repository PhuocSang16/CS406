import cv2
import numpy as np
import os

def crop_image(img , polygon):
    ## (1) Crop the bounding rect
    polygon = np.array(polygon)
    rect = cv2.boundingRect(polygon)
    x,y,w,h = rect
    croped = img[y:y+h, x:x+w].copy()
    ## (2) make mask
    polygon = polygon - polygon.min(axis=0)
    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [polygon], -1, (255, 255, 255), -1, cv2.LINE_AA)
    ## (3) do bit-op
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    return dst

def relu(x):
    return x if x >= 0 else 0

cnt = 0

for img_folder, out_path in [('vietnamese/train_images', 'vietnamese/recog_train_gt.txt'),
                            ('vietnamese/test_image', 'vietnamese/recog_val_gt.txt'),
                            ('vietnamese/unseen_test_images', 'vietnamese/recog_test_gt.txt')]:

  print(f'========== {img_folder} =============')

  wf = open(out_path, 'w', encoding='utf-8')
  img_files = sorted(os.listdir(img_folder))

  for idx, img_file in enumerate(img_files):
    if (idx + 1) % 200 == 0:
      print(f'{idx + 1}/{len(img_files)}')
    img = cv2.imread(os.path.join(img_folder, img_file))
    gt_path = os.path.join('vietnamese/labels', f'gt_{int(img_file[2:6])}.txt')

    with open(gt_path, 'r', encoding='utf-8') as rf:
      lines = rf.readlines()

    for line in lines:
      line = line.split(',', maxsplit=8)
      polygon, label = line[:8], line[8].strip()
      if label in ('###', ''):
        continue

      polygon = [[relu(int(polygon[_])), relu(int(polygon[_ + 1]))] for _ in range(0, len(polygon), 2)]

      try:
        cropped_img = crop_image(img, polygon)
        # Save
        fname = f'img{cnt:05}.jpg'
        saved_path = os.path.join('vietnamese/recog-data', fname)
        wf.write(f'{fname}\t{label}\n')
        cv2.imwrite(saved_path, cropped_img)
        cnt += 1
      except:
        print(img_file, label, polygon, img.shape)