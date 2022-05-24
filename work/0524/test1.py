import random
import os
from PIL import Image, ImageEnhance # pip install Pillow

# 새로 만들 이미지 개수 설정
num_augmented_img = 70

# 원본 사진 경로
file_path = "./image"

# 위의 폴더 내부에 있는 이미지 이름의 배열이 저장 되는 형태
file_name = os.listdir(file_path)
# print(file_name)

# file_name 길이를 가져온다.
total_origin_image_run = len(file_name)
print("total image number >>", total_origin_image_run)

augment_cnt = 1

for i in range(1, num_augmented_img+1):
    change_picture_index = random.randint(0, total_origin_image_run-1)
    file_names = file_name[change_picture_index]
    # print(file_names)

    os.makedirs("./custom_image", exist_ok=True)
    origin_image_path = "./image/" + file_names

    image = Image.open(origin_image_path)

    random_augment = random.randrange(1, 7)
    # print(random_augment)

    if(random_augment == 1): # 좌우반전
        inverted_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        inverted_image.save("./custom_image/" + "inverted_" + str(augment_cnt) + ".png")
    elif(random_augment == 2): # -20도 ~ 20도 회전
        rotated_image = image.rotate(random.randrange(-20, 20))
        rotated_image.save("./custom_image/" + "rotated_" + str(augment_cnt) + ".png")
    elif(random_augment == 3): # 리사이즈
        resized_image = image.resize(size=(224, 224))
        resized_image.save("./custom_image/" + "resized_" + str(augment_cnt) + ".png")
    elif(random_augment == 4): # 밝기 조정
        brightness_enhancer = ImageEnhance.Brightness(image)
        brighter_image = brightness_enhancer.enhance(factor=random.uniform(0.3, 1.5))
        brighter_image.save("./custom_image/" + "brightness_" + str(augment_cnt) + ".png")
    elif(random_augment == 5): # 이미지 색상 균형 조정
        changecolor_enhancer = ImageEnhance.Color(image)
        chcolor_image = changecolor_enhancer.enhance(factor=random.uniform(0.3, 1.5))
        chcolor_image.save("./custom_image/" + "chcolor_" + str(augment_cnt) + ".png")
    elif(random_augment == 6): # 대비조정 0.5 ~ 1.5
        contrast_enhancer = ImageEnhance.Contrast(image)
        contrast_image = contrast_enhancer.enhance(factor=random.uniform(0.5, 1.5))
        contrast_image.save("./custom_image/" + "contrast_" + str(augment_cnt) + ".png")
    augment_cnt += 1