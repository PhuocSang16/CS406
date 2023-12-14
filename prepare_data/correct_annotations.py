# Correct label
import cv2
import numpy as np

# ROTATE_90_COUNTERCLOCKWISE
def rotate_270(img_path):
    img = cv2.imread(img_path)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(img_path, img)

[rotate_270(img_path) for img_path in ['vietnamese/test_image/im1318.jpg',
                                       'vietnamese/test_image/im1319.jpg',
                                       'vietnamese/test_image/im1383.jpg',
                                       'vietnamese/train_images/im0211.jpg',
                                       'vietnamese/train_images/im0280.jpg',
                                       'vietnamese/train_images/im0286.jpg']]

# ROTATE_90_CLOCKWISE
def rotate_90(img_path):
  img = cv2.imread(img_path)
  img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
  cv2.imwrite(img_path, img)

[rotate_90(img_path) for img_path in ['vietnamese/test_image/im1371.jpg',
                                       'vietnamese/train_images/im0212.jpg',
                                       'vietnamese/train_images/im0219.jpg']]

# Remove polygons out of image
def remove_wrong_polygon(label_path):
  with open(label_path, 'r', encoding='utf-8') as rf:
    data = rf.readlines()

  with open(label_path, 'w', encoding='utf-8') as wf:
    for line in data:
      line = line.strip()
      if line in ('310,1218,350,1216,352,1232,308,1239,KLEIN',
                  '353,1212,388,1198,389,1216,354,1230,JEANS'):
        continue
      wf.write(line + '\n')

remove_wrong_polygon('vietnamese/labels/gt_148.txt')