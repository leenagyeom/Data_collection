import json
import pandas as pd

json_path = "./anno/raccoon_annotations.coco.json"

with open(json_path, "r") as j:
    coco_info = json.load(j)

assert len(coco_info) > 0, "파일 읽기 실패"

filename = []
bbox_x = []
bbox_y = []
bbox_h = []
bbox_w = []
for image, annotation in zip(coco_info["images"], coco_info["annotations"]):
    if image["id"] < 10:
        name = "Image_0" + str(image["id"]) + ".jpg"
    else:
        name = "Image_" + str(image["id"]) + ".jpg"
    filename.append(name)
    bbox_x.append(annotation["bbox"][0])
    bbox_y.append(annotation["bbox"][1])
    bbox_h.append(annotation["bbox"][2])
    bbox_w.append(annotation["bbox"][3])

dictionary = {
    'file_name' : filename,
    'bbox_x' : bbox_x,
    'bbox_y' : bbox_y,
    'bbox_w' : bbox_w,
    'bbox_h' : bbox_h
}

dict2df = pd.DataFrame(dictionary)
dict2df.to_csv("./이나겸.csv", index=None)
# print(dict2df)