import time

# 숙지하고 있어야하는 라이브러리
import albumentations
import cv2
from torch.utils.data import Dataset
from torchvision import transforms
from matplotlib import pyplot as plt
from albumentations.pytorch import ToTensorV2

# custom dataset
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

albumentations_dataset = AlbumentationsDataset(
    file_path=["./image/1.jpg"],
    labels=[1],
    transform=albumentations_transform
)

total_time = 0
for i in range(100):
    sample, _, transform_time = albumentations_dataset[0]
    total_time += transform_time

print("albumentation time / sample : {} ms".format(total_time*10))

plt.figure(figsize=(10,10))
plt.imshow(transforms.ToPILImage()(sample)) # sample을 어떻게 할지 생각해본다. 여러장이 되게끔..
plt.show()