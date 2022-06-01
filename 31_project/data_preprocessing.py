import os, glob, random
import cv2
import numpy as np
from PIL import Image, ImageEnhance

# padding 추가
def padding(img, set_size=255):
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


origin_path = './tropical_fruit'
mango_file = glob.glob(os.path.join(origin_path + "/mango*.png"))
dragon_file = glob.glob(os.path.join(origin_path + "/dragon*.png"))
lychee_file = glob.glob(os.path.join(origin_path + "/lychee*.png"))
durian_file = glob.glob(os.path.join(origin_path + "/durian*.png"))

file_list = [mango_file, dragon_file, lychee_file, durian_file]
for file in file_list:
    if len(file) < 150:
        for cnt in range(150 - len(file)):
            random_file_num = random.randrange(len(file))
            random_file = file[random_file_num]
            image = Image.open(random_file)
            name = random_file.split('\\')[1]
            name = name.split('.')[0]
            rand_num = random.randint(0, 3)
            if rand_num == 0:
                inverted_image = image.transpose(Image.FLIP_LEFT_RIGHT)
                inverted_image.save(os.path.join(origin_path, name + '_i.png'))
            elif rand_num == 1:
                brightness_image = ImageEnhance.Brightness(image).enhance(factor=random.uniform(0.3, 1.5))
                brightness_image.save(os.path.join(origin_path, name + '_b.png'))
            elif rand_num == 2:
                rotated_image = image.rotate(random.randrange(-20, 20))
                rotated_image.save(os.path.join(origin_path, name + '_r.png'))
            elif rand_num == 3:
                changedcolor_image = ImageEnhance.Color(image).enhance(factor=random.uniform(0.3, 1.5))
                changedcolor_image.save(os.path.join(origin_path, name + '_c.png'))

os.makedirs("./mango", exist_ok=True)
os.makedirs("./lychee", exist_ok=True)
os.makedirs("./durian", exist_ok=True)
os.makedirs("./dragon_fruit", exist_ok=True)

for idx, i in enumerate(os.listdir(origin_path)):
    open_img = cv2.imread(origin_path +f'/{i}')
    new_img = padding(open_img)
    category = i.split('.')[0].split('_')[0]

    if category == 'mango':
        cv2.imwrite(f"./mango/{category}_{idx}.png", new_img)
    elif category == 'dragon':
        cv2.imwrite(f"./dragon_fruit/{category}_{idx}.png", new_img)
    elif category == 'durian':
        cv2.imwrite(f"./durian/{category}_{idx}.png", new_img)
    elif category == 'lychee':
        cv2.imwrite(f"./lychee/{category}_{idx}.png", new_img)