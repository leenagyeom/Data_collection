import os
import torch
import glob
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset

class MyCustomDatasetImage(Dataset):
    def __init__(self, path): # 파라미터 값은 달라질 수 있다.
        # 정의
        # ./Grapevine_leaves_Image_Dataset/*/*.png
        self.all_data = sorted(glob.glob(os.path.join(path, '*', '*.png')))

    def __getitem__(self, index):
        # 정의 작성된 내용을 구현
        data_path = self.all_data[index]
        data_split = data_path.split('\\')
        # ['./Grapevine_leaves_Image_Dataset', 'Nazli', 'Nazli (96).png']
        data_labels = data_split[1]
        # print(data_labels)

        data_label = 0
        if data_labels == 'Ak':
            data_label = 0
        elif data_labels == 'Ala_Idris':
            data_label = 1
        elif data_labels == 'Buzgulu':
            data_label = 2
        elif data_labels == 'Dimnit':
            data_label = 3
        elif data_labels == 'Nazli':
            data_label = 4

        print(data_label, data_labels)

        # 이미지 오픈이 필요하다면 cv2나 PIL을 이용해서 해주면 된다.
        # cv2 -> imread / PIL -> Image.open

        return data_path, data_label

    def __len__(self):
        # 전체 길이를 반환 -> 리스트 [] len()
        return len(self.all_data)

# 2가지 구성 필요 -> dataset, dataloader
dataset = MyCustomDatasetImage(path="./Grapevine_leaves_Image_Dataset/")
dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

for path in dataloader:
    pass
    # print("path info >> ", path)
