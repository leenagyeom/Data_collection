import time

# 숙지하고 있어야하는 라이브러리
import torch
import torchvision
import cv2
import numpy as np
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
from matplotlib import pyplot as plt

# custom dataset
class TorchvisionDataset(Dataset):

    def __init__(self, file_path, labels, transform=None):
        self.file_path = file_path
        self.labels = labels
        self.transform = transform

    def __getitem__(self, index):
        label = self.labels[index]
        file_path = self.file_path[index]

        # 경로를 읽어서 image open
        image = Image.open(file_path)

        start_t = time.time()
        if self.transform:
            image = self.transform(image)
        total_time = (time.time() - start_t)

        return image, label, total_time

    def __len__(self):
        return len(self.file_path)

torchvision_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop((224, 224)), # 딥러닝 모델의 input 사이즈가 224, 224라서 보통 resize를 256, 256한 다음에 224, 224 한다.
    transforms.RandomHorizontalFlip(p=0.8), # 80% 확률로 Horizontal 일어나게, 기본은 0.5
    transforms.ToTensor()] # 마지막에 학습할때는 ToTensor로 해야한다. 이미지 형태가 Tensor로 나온다.
)

torchvision_dataset = TorchvisionDataset(
    file_path=["./image/1.jpg"],
    labels=[1],
    transform=torchvision_transform
)

total_time = 0
for i in range(100):
    sample, _, transform_time = torchvision_dataset[0]
    total_time += transform_time

print("torchvision time / sample : {} ms".format(total_time*10))

plt.figure(figsize=(10,10))
plt.imshow(transforms.ToPILImage()(sample))
plt.show()