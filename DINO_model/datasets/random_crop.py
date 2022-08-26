import PIL #version 1.2.0
import torch
import os
import torchvision.transforms.functional as F
import numpy as np
import random


def intersect(boxes1, boxes2):
    n1 = boxes1.size(0)
    n2 = boxes2.size(0)
    max_xy =  torch.min(boxes1[:, 2:].unsqueeze(1).expand(n1, n2, 2),
                        boxes2[:, 2:].unsqueeze(0).expand(n1, n2, 2))
    
    min_xy = torch.max(boxes1[:, :2].unsqueeze(1).expand(n1, n2, 2),
                       boxes2[:, :2].unsqueeze(0).expand(n1, n2, 2))
    inter = torch.clamp(max_xy - min_xy , min=0)  # (n1, n2, 2)
    return inter[:, :, 0] * inter[:, :, 1]  #(n1, n2)
def find_IoU(boxes1, boxes2):
    inter = intersect(boxes1, boxes2)
    area_boxes1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    area_boxes2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])
    
    area_boxes1 = area_boxes1.unsqueeze(1).expand_as(inter) #(n1, n2)
    area_boxes2 = area_boxes2.unsqueeze(0).expand_as(inter)  #(n1, n2)
    union = (area_boxes1 + area_boxes2 - inter)
    return inter / union


def random_crop(image, boxes, labels, difficulties=None):
    if type(image) == PIL.Image.Image:
        image = F.to_tensor(image)
    original_h = image.size(1)
    original_w = image.size(2)
    
    while True:
        mode = random.choice([0.1, 0.3, 0.5, 0.9, None])
        
        if mode is None:
            return F.to_pil_image(image), boxes, labels, difficulties
        
        new_image = image
        new_boxes = boxes
        new_difficulties = difficulties
        new_labels = labels
        for _ in range(50):
            new_h = random.uniform(0.3*original_h, original_h)
            new_w = random.uniform(0.3*original_w, original_w)
            
            if new_h/new_w < 0.5 or new_h/new_w > 2:
                continue
            
            left = random.uniform(0, original_w - new_w)
            right = left + new_w
            top = random.uniform(0, original_h - new_h)
            bottom = top + new_h
            crop = torch.FloatTensor([int(left), int(top), int(right), int(bottom)])
            
            overlap = find_IoU(crop.unsqueeze(0), boxes) 
            overlap = overlap.squeeze(0)

            if overlap.shape[0] == 0:
                continue
            if overlap.max().item() < mode:
                continue
            
            new_image = image[:, int(top):int(bottom), int(left):int(right)]
            
            center_bb = (boxes[:, :2] + boxes[:, 2:])/2.0
            
            center_in_crop = (center_bb[:, 0] >left) * (center_bb[:, 0] < right
                             ) *(center_bb[:, 1] > top) * (center_bb[:, 1] < bottom) 
            
            if not center_in_crop.any():
                continue
            
            new_boxes = boxes[center_in_crop, :]
            
            new_labels = labels[center_in_crop]
            
            if difficulties is not None:
                new_difficulties = difficulties[center_in_crop]
            else:
                new_difficulties = None
            
            new_boxes[:, :2] = torch.max(new_boxes[:, :2], crop[:2])
            
            new_boxes[:, :2] -= crop[:2]
            
            new_boxes[:, 2:] = torch.min(new_boxes[:, 2:],crop[2:])
            
            new_boxes[:, 2:] -= crop[:2]
            
            return F.to_pil_image(new_image), new_boxes, new_labels, new_difficulties