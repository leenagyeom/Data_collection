import os
import cv2
import glob
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from torchvision.utils import save_image

class MyCustomDataset(Dataset):
    def __init__(self, path, transform = None):
        # ./preprocessing\\dragon_90.png
        self.all_data = glob.glob(os.path.join(path, '*.png'))
        self.transform = transform

    def __getitem__(self, index):
        data_path = self.all_data[index]
        image = Image.open(data_path)

        if self.transform:
            image = self.transform(image)
            # print(image.shape)
            # exit()
        data_split = data_path.split('\\')
        data_labels = data_split[1].split('.')[0].split('_')[0]

        data_label = 0
        if data_labels == 'mango':
            data_label = 0
        elif data_labels == 'dragon':
            data_label = 1
        elif data_labels == 'lychee':
            data_label = 2
        elif data_labels == 'durian':
            data_label = 3

        return image, data_path, data_label

    def __len__(self):
        return len(self.all_data)

torchvision_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomCrop((224, 224)),
    transforms.RandomHorizontalFlip(p=0.8),
    transforms.ToTensor()]
)

# train, valid, test 데이터 split
# train : 550 / valid : 62 / test : 68
dataset = MyCustomDataset(
    path="./preprocessing/",
    transform = torchvision_transform
)
tv_data,test = train_test_split(dataset, test_size=0.1, shuffle=True)
train,valid = train_test_split(tv_data, test_size=0.1, shuffle=True)

train_dataloader = DataLoader(train, batch_size=1, shuffle=False)
valid_dataloader = DataLoader(valid, batch_size=1, shuffle=False)
test_dataloader = DataLoader(test, batch_size=1, shuffle=False)


# 이미지, 라벨 출력 확인
for (n, v, t) in zip(train_dataloader, valid_dataloader, test_dataloader):
    print("image >>", n[1], "\tlabel >>", n[2])
    print("image >>", v[1], "\tlabel >>", v[2])
    print("image >>", t[1], "\tlabel >>", t[2])


# dataset - train, valid, test 폴더 구성
os.makedirs('./dataset/train', exist_ok=True)
os.makedirs('./dataset/valid', exist_ok=True)
os.makedirs('./dataset/test', exist_ok=True)

for train in train_dataloader:
    n_filename = train[1][0].split('\\')[1]
    save_image(train[0][0], f'./dataset/train/{n_filename}')

for valid in valid_dataloader:
    v_filename = valid[1][0].split('\\')[1]
    save_image(valid[0][0], f'./dataset/valid/{v_filename}')

for test in test_dataloader:
    t_filename = test[1][0].split('\\')[1]
    save_image(test[0][0], f'./dataset/test/{t_filename}')