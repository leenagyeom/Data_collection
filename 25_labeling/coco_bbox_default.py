import os
import json
import cv2

json_path = "./json_data/instances_default.json"

with open(json_path, "r") as j:
    coco_info = json.load(j)

# print(coco_info)

# 예외처리
# 현재 파일을 읽지 못하면 여기서 종료된다.
assert len(coco_info) > 0, "파일 읽기 실패"

# 카테고리 정보 수집
categories = dict()
for category in coco_info['categories']:
    categories[category["id"]] = category["name"]

# print("categories info >>", categories)

# annotation 정보 저장
annotation_info = dict()
for annotation in coco_info['annotations']:
    # print("annotation info >>", annotation)
    image_id    = annotation["image_id"]
    bbox        = annotation["bbox"]
    category_id = annotation["category_id"]

    # print("bbox info >>", bbox)
    if image_id not in annotation_info:
        annotation_info[image_id] = {"boxes" : [bbox],
                                     "categories" : [category_id]}
    else :
        annotation_info[image_id]["boxes"].append(bbox)
        annotation_info[image_id]["categories"].append(categories[category_id])
    # print(annotation_info)

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

    try:
        annotation = annotation_info[img_id]
    except KeyError:
        continue

    print(annotation)
    for bbox, category in zip(annotation["boxes"], annotation["categories"]):
        x1, y1, w, h = bbox

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2

        org_img = img.copy()

        # if category == 1:
        #     category = "ros"

        text_img = cv2.putText(img, str(category),
                               (int(x1), int(y1)-10), font, fontScale, color, thickness, cv2.LINE_AA)

        rec_img = cv2.rectangle(text_img, (int(x1), int(y1)), (int(x1+w), int(y1+h)), (255, 0, 255), 2)
        cv2.imshow("test", rec_img)
        cv2.waitKey(0)