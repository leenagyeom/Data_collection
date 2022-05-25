import os
import json
import cv2
import numpy as np
from torch.utils.data import Dataset
import glob

json_path = "./anno/raccoon_annotations.coco.json"
with open(json_path, "r") as j:
    coco_info = json.load(j)

# 예외처리
# 현재 파일을 읽지 못하면 여기서 종료된다.
assert len(coco_info) > 0, "파일 읽기 실패"

def padding(img, set_size=225):

    percent = 1
    if(img.shape[1] > img.shape[0]):
        percent = 255 / img.shape[1]
    else:
        percent = 255 / img.shape[0]

    img = cv2.resize(img, dsize=(0, 0), fx=percent, fy=percent, interpolation=cv2.INTER_LINEAR)

    y, x, h, w = (0, 0, img.shape[0], img.shape[1])

    w_x = (255 - (w - x)) / 2
    h_y = (255 - (h - y)) / 2

    if (w_x < 0):
        w_x = 0
    elif (h_y < 0):
        h_y = 0

    M = np.float32([[1, 0, w_x], [0, 1, h_y]])
    img_re = cv2.warpAffine(img, M, (255, 255))

    return img_re

class myCustomDataset(Dataset):
    def __init__(self, path):
        self.data = sorted(glob.glob(os.path.join(path, '*.json')))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):

        annotation_info = dict()
        for annotation in coco_info['annotations']:
            image_id = annotation["image_id"]
            bbox = annotation["bbox"]

            if image_id not in annotation_info:
                annotation_info[image_id] = {"boxes": bbox}
            else:
                annotation_info[image_id]["boxes"].append(bbox)

        filelist = []
        for image_info in coco_info['images']:
            filename = image_info["file_name"]
            filepath = os.path.join("./data", filename)
            filelist.append([filename, filepath])

        return annotation_info, filelist

dataset = myCustomDataset(path="./anno/")
os.makedirs("./newImage_dataset", exist_ok=True)

annotation_information = list(dataset[0][0].values())
filelist_information = dataset[0][1]

for ann, file in zip(annotation_information, filelist_information):
    [x, y, w, h] = ann.get('boxes')
    file_path = file[1]
    img = cv2.imread(file_path)

    dst = img[int(y) : int(y+h), int(x) : int(x+w)].copy()
    new_img = padding(dst)
    cv2.imshow("new image", new_img)
    cv2.imwrite(f"./newImage_dataset/{file[0]}", new_img)
    cv2.waitKey(0)