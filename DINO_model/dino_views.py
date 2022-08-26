from unittest import result
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

import os, sys
import torch, json
import numpy as np

from main import build_model_main
from util.slconfig import SLConfig
from datasets import build_dataset
from util.visualizer import COCOVisualizer
from util import box_ops

from PIL import Image
import datasets.transforms as T
import urllib
import base64
from io import BytesIO

# config 파일 경로
model_config_path = "../DINO_model/config/DINO/DINO_4scale.py"
# 학습 체크포인트 파일 경로
model_checkpoint_path = "../DINO_model/ckpts/20_checkpoint_best_regular.pth"

args = SLConfig.fromfile(model_config_path) 
args.device = 'cuda' 
model, criterion, postprocessors = build_model_main(args)
checkpoint = torch.load(model_checkpoint_path, map_location='cpu')
model.load_state_dict(checkpoint['model'])
_ = model.eval()

# id 클래스 대치 파일
with open('../DINO_model/util/20class_plant_coco_id2name.json') as f:
    id2name = json.load(f)
    id2name = {int(k):v for k,v in id2name.items()}


def dino_api(request):
    if request.method == 'POST':
        imageURL = request.body.decode()
        openedURL = urllib.request.urlopen(imageURL)
        with open('image.jpeg', 'wb') as f:
            f.write(openedURL.file.read())

        image = Image.open('image.jpeg').convert("RGB")
        imgDPI = 96
        imgWidth, imgHeight = image.size

        transform = T.Compose([
            T.RandomResize([800], max_size=1333),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        image, _ = transform(image, None)

        model.eval()
        with torch.no_grad():
            output = model.cuda()(image[None].cuda())
            output = postprocessors['bbox'](output, torch.Tensor([[1.0, 1.0]]).cuda())[0]

        threshold = 0.2 # threshold 조절

        vslzr = COCOVisualizer()

        scores = output['scores']
        labels = output['labels']
        boxes = box_ops.box_xyxy_to_cxcywh(output['boxes'])
        select_mask = scores > threshold
        print(scores[select_mask])

        # 같은 bbox에 중복 label 제거
        dupBoxes = boxes[select_mask].tolist()
        for i, bbox in enumerate(dupBoxes):
            if bbox in dupBoxes[:i]:
                select_mask[i] = False

        box_label = [id2name[int(item)] for item in labels[select_mask]]
        pred_dict = {
            'boxes': boxes[select_mask],
            'size': torch.Tensor([image.shape[1], image.shape[2]]),
            'box_label': box_label
        }
        resultImg = vslzr.visualize(image, pred_dict, savedir=None, dpi=imgDPI, show_in_console=False, width=imgWidth, height=imgHeight)
        buffered = BytesIO()
        resultImg.save(buffered, format='PNG')
        data64 = base64.b64encode(buffered.getvalue())
        resultImgURL = u'data:image/png;base64,' + data64.decode('utf-8')
        print(box_label)
        print(pred_dict['boxes'])

        # etc 및 중복 버튼 제거
        labelJson = []
        for label in box_label:
            if label not in labelJson and label != 'etc':
                labelJson.append(label)

        # API JSON
        sendJson = {}
        sendJson['image'] = resultImgURL
        sendJson['labels'] = labelJson

        return JsonResponse(sendJson)