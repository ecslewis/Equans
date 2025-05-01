import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform= transforms.Compose([transforms.Resize((64,64)), transforms.ToTensor(), transforms.RandomHorizontalFlip(), transforms.RandomRotation(10),transforms.Normalize((0.5,),(0.5,))])



train_dataset= datasets.ImageFolder('data/train', transform=transform)
train_loader= DataLoader(train_dataset, batch_size=32, shuffle=True)

test_dataset = datasets.ImageFolder('data/test', transform=transform)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

__path__='data/test'
