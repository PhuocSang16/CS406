import os
import json
import cv2
import numpy as np

PRED_FOLDER = 'result/preds'
GT_FOLDER = '../vietnamese/labels'
IMG_FOLDER = '../vietnamese/unseen_test_images'
OUT_FOLDER = 'visual_res'
thrs = 0.7

def draw_pred_polygon(img, polygon):
    h, w, _ = img.shape
    polygon = [[max(min(int(polygon[i]), w), 0),
                        max(min(int(polygon[i + 1]), h), 0)] 
                        for i in range(0, len(polygon), 2)]

    polygon = np.array(polygon, dtype=np.int32)
    polygon = polygon.reshape((-1, 1, 2))

    isClosed = True
    color = (0, 255, 0)
    thickness = 2

    overlay = img.copy()
    overlay= cv2.polylines(overlay, [polygon], 
                      isClosed, color, 
                      thickness)

    return cv2.addWeighted(overlay, 0.4, img, 0.6, 0) 

def draw_gt_polygon(img, polygon):
    h, w, _ = img.shape
    polygon = [[max(min(int(polygon[i]), w), 0),
                        max(min(int(polygon[i + 1]), h), 0)] 
                        for i in range(0, len(polygon), 2)]

    polygon = np.array(polygon, dtype=np.int32)
    color = (0, 0, 255)

    overlay = img.copy()
    cv2.drawContours(overlay, [polygon], -1, color, -1)

    return cv2.addWeighted(overlay, 0.3, img, 0.7, 0) 

# Loop fname
pnames = sorted(os.listdir(PRED_FOLDER))
for pname in pnames:
    ppath = os.path.join(PRED_FOLDER, pname)

    iname = pname.split('.')[0] + '.jpg'
    ipath = os.path.join(IMG_FOLDER, iname)

    gname = 'gt_' + pname.split('.')[0][2:] + '.txt'
    gpath = os.path.join(GT_FOLDER, gname)

    # Read pred content
    with open(ppath, 'r') as rf:
        content = json.load(rf)
        pred_bboxes = content['det_polygons']
        pred_scores = content['det_scores']
    
    # Read gt content
    gt_bboxes = []
    with open(gpath, 'r', encoding='utf-8') as rf:
        for line in rf.readlines():
            bbox = list(map(int, line.split(',', maxsplit=8)[:8]))
            gt_bboxes.append(bbox)

    img = cv2.imread(ipath)

    # Draw pred polygon
    for bbox, score in zip(pred_bboxes, pred_scores):
        if score >= thrs:
            img = draw_pred_polygon(img, bbox)
    
    # Draw gt polygon
    for bbox in gt_bboxes:
        img = draw_gt_polygon(img, bbox)

    oiname = os.path.join(OUT_FOLDER, iname)
    cv2.imwrite(oiname, img)