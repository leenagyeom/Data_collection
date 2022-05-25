import os
import json
import cv2
import numpy as np

json_path = "./json_data/instances_polygon.json"

with open(json_path, "r") as j:
    coco_info = json.load(j)

# print(coco_info)

# 예외처리
# 현재 파일을 읽지 못하면 여기서 종료된다.
assert len(coco_info) > 0, "파일 읽기 실패"

# 카테고리 정보 수집
categories = dict()
for cat in coco_info['categories']:
    categories[cat["id"]] = cat["name"]
    # 1 : rose
# print("categories info >>", categories)

# annotation 정보 저장
annotation_info = dict()
for anno in coco_info['annotations']:
    # print("annotation info >>", anno)
    image_id     = anno["image_id"]
    bbox         = anno["bbox"]
    category_id  = anno["category_id"]
    segmentation = anno["segmentation"]

    # print("anno info >>", anno["segmentation"])
    if image_id not in annotation_info:
        annotation_info[image_id] = {"boxes" : [bbox],
                                     "categories" : [category_id],
                                     "segmentation" : [segmentation]
                                     }
    else :
        annotation_info[image_id]["boxes"].append(bbox)
        annotation_info[image_id]["categories"].append(categories[category_id])
        annotation_info[image_id]["segmentation"].append(categories[category_id])

    print(annotation_info)


for image_info in coco_info['images']:
    filename = image_info["file_name"]
    height   = image_info["height"]
    width    = image_info["width"]
    img_id = image_info["id"]
    # print(filename, height, width)

    file_path = os.path.join("./image_data", filename)
    # print(file_path)

    # image read
    img = cv2.imread(file_path)

    # try:
    #     annotation = annotation_info[img_id]
    # except KeyError:
    #     continue

    # print(annotation)
    print(annotation_info[image_id])
    for bbox, category, segmentation in zip(annotation_info[image_id]["boxes"], annotation_info[image_id]["categories"], annotation_info[image_id]["segmentation"]):
        x1, y1, w, h = bbox

        for seg in segmentation:
            poly = np.array(seg, np.int32).reshape((int(len(seg)/2), 2)) # 1차원으로 바꾼것을 두개씩만 가져와야한다. (x, y) 형태로
            poly_img = cv2.polylines(img, [poly], True, (255, 0, 0), 2)
            cv2.imshow("test", poly_img)
            cv2.waitKey(0)