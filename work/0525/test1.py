import os
import json
import cv2
import numpy as np

json_path = "./anno/raccoon_annotations.coco.json"

with open(json_path, "r") as j:
    coco_info = json.load(j)

assert len(coco_info) > 0, "파일 읽기 실패"

def padding(img, set_size=225):
    percent = 1
    if(img.shape[1] > img.shape[0]):
        percent = set_size / img.shape[1]
    else:
        percent = set_size / img.shape[0]

    img = cv2.resize(img, dsize=(0, 0), fx=percent, fy=percent, interpolation=cv2.INTER_LINEAR)
    y, x, h, w = (0, 0, img.shape[0], img.shape[1])

    w_x = (set_size - (w - x)) / 2
    h_y = (set_size - (h - y)) / 2

    if (w_x < 0):
        w_x = 0
    elif (h_y < 0):
        h_y = 0

    M = np.float32([[1, 0, w_x], [0, 1, h_y]])
    img_re = cv2.warpAffine(img, M, (set_size, set_size))
    return img_re

categories = dict()
for cate in coco_info['categories']:
    categories[cate["id"]] = cate["name"]

annotation_info = dict()
for annotation in coco_info['annotations']:
    image_id    = annotation["image_id"]
    bbox        = annotation["bbox"]

    if image_id not in annotation_info:
        annotation_info[image_id] = {"boxes" : [bbox]}
    else :
        annotation_info[image_id]["boxes"].append(bbox)

filelist = []
for image_info in coco_info['images']:
    filename = image_info["file_name"]
    img_id   = image_info["id"]
    file_path = os.path.join("./data", filename)

    img = cv2.imread(file_path)

    try:
        annotation = annotation_info[img_id]
    except KeyError:
        continue

    os.makedirs("./newImage", exist_ok=True)
    for bbox in annotation["boxes"]:
        x1, y1, w, h = bbox

        dst = img[int(y1) : int(y1+h), int(x1) : int(x1+w)].copy()
        new_img = padding(dst)
        cv2.imshow("new image", new_img)
        cv2.imwrite(f"./newImage/{filename}", new_img)
        cv2.waitKey(0)