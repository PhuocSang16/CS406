#!/usr/bin/env python3
# Scene Text Recognition Model Hub
# Copyright 2022 Darwin Bautista
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

import torch

from PIL import Image

from strhub.data.module import SceneTextDataModule
from strhub.models.utils import load_from_checkpoint, parse_model_args
import os

@torch.inference_mode()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('checkpoint', help="Model checkpoint (or 'pretrained=<model_id>')")
    parser.add_argument('--images', help='Images to read')
    parser.add_argument('--outfile', help='output path')
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--batch_size', type=int, default=1)
    args, unknown = parser.parse_known_args()
    kwargs = parse_model_args(unknown)
    print(f'Additional keyword arguments: {kwargs}')

    model = load_from_checkpoint(args.checkpoint, **kwargs).eval().to(args.device)
    img_transform = SceneTextDataModule.get_transform(model.hparams.img_size)

    wf = open(args.outfile, 'w', encoding='utf-8')
    wwf = open('wrong_predicitons.txt', 'w', encoding='utf-8')

    fname_list = []
    lbl_list = []
    with open('../vietnamese/recog_test_gt.txt', 'r', encoding='utf-8') as rf:
        for line in rf.readlines():
            # print(line)
            fname, lbl = line.split(maxsplit=1)
            fname_list.append(fname)
            lbl_list.append(lbl.strip())

    fname_batches = [fname_list[i: i + args.batch_size] for i in range(0, len(fname_list), args.batch_size)]
    lbl_batches = [lbl_list[i: i + args.batch_size] for i in range(0, len(lbl_list), args.batch_size)]

    for idx, (fname_batch, lbl_batch) in enumerate(zip(fname_batches, lbl_batches)):
        img_batch = []
        for fname in fname_batch:
            # Load image and prepare for input
            image = Image.open(os.path.join(args.images, fname)).convert('RGB')
            image = img_transform(image).unsqueeze(0).to(args.device)
            img_batch.append(image)
        
        img_batch = torch.cat(img_batch)
        probs = model(img_batch).softmax(-1)
        preds, probs = model.tokenizer.decode(probs)

        for pred, fname, lbl in zip(preds, fname_batch, lbl_batch):
            wf.write(f'{fname}\t{pred}\n')
            if pred != lbl:
                wwf.write(f'{fname}\t{pred}\t{lbl}\n')

        print(f'{idx}/{len(fname_batches)}')
    wf.close()
    wwf.close()

if __name__ == '__main__':
    main()
