import torchvision.utils
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
from urllib.request import (urlopen, urlparse, urlretrieve)

import time
import albumentations
import cv2
from torch.utils.data import Dataset
from torchvision import transforms
from matplotlib import pyplot as plt
from albumentations.pytorch import ToTensorV2

chrome_path = "./chromedriver.exe"
base_url = "https://www.google.co.kr/imghp"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("lang=ko_kr")
chrome_options.add_argument("window-size=1920x1080")


def selenium_scroll_option():
    SCROLL_PAUSE_SEC = 3
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

a = "사과"
image_name = "apple"
driver = webdriver.Chrome(chrome_path)
driver.get("http://www.google.co.kr/imghp?hl=ko")
browser = driver.find_element_by_name('q')
browser.send_keys(a)
browser.send_keys(Keys.RETURN)

selenium_scroll_option()
driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
selenium_scroll_option()

image = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

image_url = []
for i in image:
    if i.get_attribute("src") != None:
        image_url.append(i.get_attribute("src"))
    else:
        image_url.append(i.get_attribute("data-src"))

# print(f"전체 다운로드한 이미지 개수 : {len(image_url)}")
image_url = pd.DataFrame(image_url)[0].unique()

os.makedirs("./apple", exist_ok=True)
apple = "./apple"
if image_name == 'apple':
    for t, url in enumerate(image_url, 0):
        print(url)
        urlretrieve(url, apple + "\\" + image_name + "_" + str(t) + ".png")
    driver.close()
print("이미지 크롤링 완료")

class AlbumentationsDataset(Dataset):
    def __init__(self, file_path, labels, transform=None):
        self.file_path = file_path
        self.labels = labels
        self.transform = transform

    def __getitem__(self, index):
        label = self.labels[index]
        file_path = self.file_path[index]

        # 경로를 읽어서 image open
        # image open이 안되서 cv2로 열어야한다.
        image = cv2.imread(file_path)

        # cv2는 이미지를 읽을때 brg로 읽어서 rgb로 바꿔줘야한다.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        start_t = time.time()
        if self.transform:
            augmented = self.transform(image = image)
            image = augmented['image']

        total_time = (time.time() - start_t)

        return image, label, total_time

    def __len__(self):
        return len(self.file_path)

albumentations_transform = albumentations.Compose([
    albumentations.Resize(256, 256),
    albumentations.RandomCrop(224, 224),
    albumentations.HorizontalFlip(),
    ToTensorV2()
])

file_list = os.listdir("./apple")
nfile_list = []
label = []
for idx, filename in enumerate(file_list):
    nfile_list.append("./apple/" + filename)
    label.append(idx)
print(nfile_list)
# print(len(file_list))

albumentations_dataset = AlbumentationsDataset(
    file_path=nfile_list,
    labels=label,
    transform=albumentations_transform
)

sample_image = []
total_time = 0

for i in range(len(nfile_list)):
    sample, _, _ = albumentations_dataset[i]
    sample_image.append(sample)

os.makedirs("./augmentation_image", exist_ok=True)
for idx, img in enumerate(sample_image):
    image = transforms.ToPILImage()(img)
    image.save(os.path.join("./augmentation_image", f"apple_{idx}.png"))
    # torchvision.utils.save_image(image, os.path.join("./augmentation_image", f"apple_{idx}.png"))