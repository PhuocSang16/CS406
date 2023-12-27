import sys
sys.path.append('./mmocr')
sys.path.append('./parseq')

from mmocr.apis.inferencers import MMOCRInferencer
import cv2
import numpy as np
import torch
from PIL import Image
from strhub.data.module import SceneTextDataModule
from strhub.models.utils import load_from_checkpoint, parse_model_args

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

class SceneTextPipeline:
    def __init__(self, det_config, det_ckpt_path, recog_ckpt_path,
                 device='cuda', batch_size=10, thresh=0.6):
        self.device = device
        self.det = self.build_detector(det_config, det_ckpt_path)
        self.recog, self.recog_img_transform = self.build_recognizer(recog_ckpt_path)
        self.thresh = thresh
        self.batch_size = batch_size

    def __call__(self, inputs):
        '''
            inputs: list các numpy array (image)

            return a list with format [
                # This dictionary is 1st image
                {
                    'det_polygons': [
                        # This is 1st polygon
                        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
                        # This is 2nd polygon
                        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]], 
                        ...
                    ],
                    'det_scores': [ # This is probabilies of detection
                        prob1, prob2, ...
                    ]
                    'texts': [
                        str1, str2, ...
                    ],
                    'recog_scores: [ # This is probabilies of recognition
                        prob1, prob2, ...
                    ]
                },
                # This dictionary is 2nd image
                {
                    ...
                }, 
                ...
            ]
        '''

        results = []

        for input in inputs:
            ### Detection
            result = self.det(inputs=input, batch_size=1)
            result = self.postprocess_det(result, input)

            ### Recognition
            # Group into batches 
            result['texts'] = []
            result['recog_scores'] = []
            poly_batches = [result['det_polygons'][i: i + self.batch_size] for i in range(0, len(result['det_polygons']), self.batch_size)]

            for poly_batch in poly_batches:
                img_batch = []
                for polygon in poly_batch:
                    image = crop_image(input, polygon)
                    image = Image.fromarray(image) # recog_img_transform require PIL Image
                    image = self.recog_img_transform(image).unsqueeze(0).to(self.device)
                    img_batch.append(image)
                
                img_batch = torch.cat(img_batch)
                probs = self.recog(img_batch).softmax(-1)
                preds, probs = self.recog.tokenizer.decode(probs)

                for pred, prob in zip(preds, probs):
                    result['texts'].append(pred)
                    result['recog_scores'].append(min(prob.cpu().detach().numpy()))

            h, w, _ = input.shape
            result['width'] = w
            result['height'] = h
            results.append(result)

        return results
    def build_detector(self, config, ckpt_path):
        init_args = {
            'det': config, 
            'det_weights': ckpt_path, 
            'rec': None, 
            'rec_weights': None, 
            'kie': None, 
            'kie_weights': None,
            'device': 'cuda'
        }

        return MMOCRInferencer(**init_args)

    def build_recognizer(self, ckpt_path):
        model = load_from_checkpoint(ckpt_path).eval().to(self.device)
        img_transform = SceneTextDataModule.get_transform(model.hparams.img_size)
        return model, img_transform
    
    def postprocess_det(self, preds, raw_image):
        '''
            preds: output of detector with format: {
                "predictions": [
                    // Image 1
                    {
                        "det_polygons": [
                            // Each bbox is a list
                            [bbox1],
                            [bbox2],... 
                        ],
                        "det_scores": [
                            score1,
                            score2,...
                        ]
                    }, 
                    {
                        "det_polygons": [
                            // Each bbox is a list
                            [bbox1],
                            [bbox2],... 
                        ],
                        "det_scores": [
                            score1,
                            score2,...
                        ]
                    }, // Image 2
                    ...
                ],
                visualizations: []
            }
            but we only process 1 image

            thresh (float): threshold
        '''
        result = {'det_polygons': [], 'det_scores': []}
        polygons = preds['predictions'][0]['det_polygons']
        scores = preds['predictions'][0]['det_scores']
        h, w, _ = raw_image.shape

        for polygon, score in zip(polygons, scores):
            if score < self.thresh:
                continue

            polygon = [[max(min(int(polygon[i]), w), 0),
                        max(min(int(polygon[i + 1]), h), 0)] 
                        for i in range(0, len(polygon), 2)]

            result['det_polygons'].append(polygon)
            result['det_scores'].append(score)
        
        return result

if __name__ == '__main__':
    # image must be numpy array
    fname = '/mmlabworkspace/Students/visedit/AIC2021/vietnamese/test_image/im1201.jpg'
    image = np.asarray(Image.open(fname).convert('RGB'))

    pipeline = SceneTextPipeline()
    print(pipeline([image]))
