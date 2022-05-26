import torchvision
import requests
from PIL import Image
import io
import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_image_from_url(url):
    response = requests.get(url)
    img_pil = Image.open(io.BytesIO(response.content)) # 이미지를 받을 때 byte로 받는 것
                                                       # byte로 받은 것을 np로 처리해야한다.
    return np.array(img_pil)

# image url
cat_url = "http://s10.favim.com/orig/160416/cute-cat-sleep-omg-Favim.com-4216420.jpeg"
dog_url = "http://s7.favim.com/orig/150714/chien-cute-dog-golden-retriever-Favim.com-2956014.jpg"

cat_img = get_image_from_url(cat_url)
dog_img = get_image_from_url(dog_url)

def mixup(x1, x2, y1, y2, lambda_=0.2):
    x = lambda_ * x1 + (1-lambda_) * x2 # 믹스업 할 때 공식, 논문에 그대로 나온다.
    y = lambda_ * y1 + (1-lambda_) * y2
    return x, y

x, y = mixup(cat_img, dog_img, np.array([1,0]), np.array([0,1]))

plt.axis('off')
plt.imshow(x.astype(int)), y
plt.show()
# np.array에서 첫번째 = cat label, 두번째(0) = dog label

# cv2.COLOR_BGR2RGB를 하지 않으면 색상이 이상하게 나온다.
# cat_img = cv2.cvtColor(cat_img, cv2.COLOR_BGR2RGB)W
# cv2.imshow("Test", cat_img)
# cv2.waitKey(0)