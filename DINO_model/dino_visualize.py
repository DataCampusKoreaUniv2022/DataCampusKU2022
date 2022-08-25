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


model_config_path = "config/DINO/DINO_4scale.py" # change the path of the model config file
model_checkpoint_path = "ckpts/20_checkpoint_best_regular.pth" # change the path of the model checkpoint
# See our Model Zoo section in README.md for more details about our pretrained models.

args = SLConfig.fromfile(model_config_path) 
args.device = 'cuda' 
model, criterion, postprocessors = build_model_main(args)
checkpoint = torch.load(model_checkpoint_path, map_location='cpu')
model.load_state_dict(checkpoint['model'])
_ = model.eval()

with open('util/20class_plant_coco_id2name.json') as f:
    id2name = json.load(f)
    id2name = {int(k):v for k,v in id2name.items()}


def visResult(path:str, savedir:str = None, num:str = None, SIC:bool = True):
    image = Image.open(path).convert("RGB") # load image

    # transform images
    transform = T.Compose([
        T.RandomResize([800], max_size=1333),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image, _ = transform(image, None)

    # predict images
    model.eval()
    with torch.no_grad():
        output = model.cuda()(image[None].cuda())
        output = postprocessors['bbox'](output, torch.Tensor([[1.0, 1.0]]).cuda())[0]

    # visualize outputs
    thershold = 0.3 # set a thershold

    vslzr = COCOVisualizer()

    scores = output['scores']
    labels = output['labels']
    boxes = box_ops.box_xyxy_to_cxcywh(output['boxes'])
    select_mask = scores > thershold

    box_label = [id2name[int(item)] for item in labels[select_mask]]
    pred_dict = {
        'boxes': boxes[select_mask],
        'size': torch.Tensor([image.shape[1], image.shape[2]]),
        'box_label': box_label,
        'image_id': num
    }
    # print(scores)
    vslzr.visualize(image, pred_dict, savedir=savedir, dpi=100, show_in_console=SIC)

for i in range(1, 17):
    imgPath = f'imagetest/{i}.jpg'
    visResult(imgPath, 'dinoresult', i, False)