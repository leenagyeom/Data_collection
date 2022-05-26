import os

import cv2.cv2
import numpy as np
import random
import cv2
import matplotlib.pyplot as plt

image_path = "./cutmix_image"
index_len = len(os.listdir(image_path))
image_list = os.listdir(image_path)

def load_image(path, index):
    image = cv2.imread(os.path.join(path, image_list[index]), cv2.cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image /= 255.0

    return image

image = load_image(image_path, 3) # 이미지 개수가 늘어나면 3을 변경해준다. 이미지는 0~3 4개이다.
image_size = image.shape[0]

def cutmix(path, index, imsize):
    w, h = imsize, imsize
    s = imsize // 2

    # 중앙값 랜덤 하게 잡기
    xc, yc = [int(random.uniform(imsize*0.25, imsize*0.75))
              for _ in range(2)] # 256 ~ 768

    indexes = [index] + [random.randint(0, index) for _ in range(3)]

    # 검은색 배경의 임의 이미지 생성 (여기다가 이미지를 붙여넣는 방식)
    return_image = np.full((imsize, imsize, 3), 1, dtype=np.float32) # 3채널짜리 이미지

    for i, index in enumerate(indexes):
        image = load_image(path, index)

        # top left
        if i == 0:
            x1a ,y1a, x2a, y2a = max(xc - w, 0), max(yc - h, 0), xc, yc
            #samll image
            x1b, y1b, x2b, y2b = w - (x2a - x1a), h - (y2a - y1a), w, h

        #top right:
        elif i == 1:
            x1a ,y1a, x2a, y2a = xc, max(yc-h, 0), min(xc+w, s*2), yc
            x1b, y1b, x2b, y2b = 0, h - (y2a - y1a), min(w, x2a - x1a), h

        # bottom left:
        elif i == 2:
            x1a ,y1a, x2a, y2a = max(xc - w, 0), yc, xc, min(s * 2, yc + h)
            x1b, y1b, x2b, y2b = w - (x2a - x1a), 0, max(xc, w), min(y2a - y1a, h)

        elif i == 3:
            x1a ,y1a, x2a, y2a = xc, yc, min(xc + w, s * 2), min(s * 2, yc + h)
            x1b, y1b, x2b, y2b = 0, 0, min(w, x2a - x1a), min(y2a - y1a, h)

        return_image[y1a:y2a, x1a:x2a] = image[y1b:y2b, x1b:x2b]
    return return_image

test = cutmix(image_path, 3, image_size)
plt.imshow(test)
plt.show()