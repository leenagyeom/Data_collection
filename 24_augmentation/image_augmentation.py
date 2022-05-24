import random
import numpy as np
import os
import cv2            # pip install opencv-python
import glob
from PIL import Image # pip install Pillow
import PIL.ImageOps

# 새로 만들 이미지 개수 설정
num_augmented_img = 50

# 원본 사진 경로
file_path = "./image"

# 위의 폴더 내부에 있는 이미지 이름의 배열이 저장 되는 형태
file_name = os.listdir(file_path)
# print(file_name)

# file_name 길이를 가져온다.
total_origin_image_run = len(file_name)
print("total image number >>", total_origin_image_run)

augment_cnt = 1

for i in range(1, num_augmented_img):
    change_picture_index = random.randint(1, total_origin_image_run-1)
    # print(change_picture_index)
    file_names = file_name[change_picture_index]
    # print(file_names)

    os.makedirs("./custom_image", exist_ok=True)
    origin_image_path = "./image/" + file_names
    # print(origin_image_path)

    image = Image.open(origin_image_path)

    # 랜덤 값이 1~4 사이의 값이 나오도록 1, 2, 3
    random_augment = random.randint(1, 4)
    # print(random_augment)

    if(random_augment == 1):
        # 이미지 좌우 반전
        inverted_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        inverted_image.save("./custom_image/" + "inverted_" + str(augment_cnt) + ".png")
    elif(random_augment == 2):
        # 이미지 기울기
        rotated_image = image.rotate(random.randrange(-20, 20))
        rotated_image.save("./custom_image/" + "rotated_" + str(augment_cnt) + ".png")
    elif(random_augment == 3):
        # 이미지 resize
        resized_image = image.resize(size=(224, 224))
        resized_image.save("./custom_image/" + "resized_" + str(augment_cnt) + ".png")
    augment_cnt += 1