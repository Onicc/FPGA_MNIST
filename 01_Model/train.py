import os
from tqdm import tqdm
import numpy as np
import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn

from net import Net_DW, Net_DW_Branch

CIFAR100_TRAIN_MEAN = (0.1307)
CIFAR100_TRAIN_STD = (0.3081)
MILESTONES = [2, 5, 8]

if __name__ == "__main__":
    gpu = True
    num_classes = 10
    batch_size = 64
    lr = 0.01
    Epoch = 200
    model_path = ""
    checkpoint_path = "01_Model/models"

    # 这里加载的数据是归一化后的，最大值为0
    train_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST('00_Data', train=True, download=True,
                                transform=torchvision.transforms.Compose([
                                    torchvision.transforms.ToTensor(),
                                    # torchvision.transforms.Normalize(
                                    #     CIFAR100_TRAIN_MEAN, CIFAR100_TRAIN_STD)
                                ])),
        batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST('00_Data', train=False, download=True,
                                transform=torchvision.transforms.Compose([
                                    torchvision.transforms.ToTensor(),
                                    # torchvision.transforms.Normalize(
                                    #     CIFAR100_TRAIN_MEAN, CIFAR100_TRAIN_STD)
                                ])),
        batch_size=batch_size, shuffle=True)
    
    model = Net_DW_Branch()
    net_name = "Net_DW_Branch"
    if gpu:
        model = model.cuda()

    if model_path != '':
        print('Load weights {}.'.format(model_path))
        device          = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model_dict      = model.state_dict()
        pretrained_dict = torch.load(model_path, map_location = device)
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if np.shape(model_dict[k]) == np.shape(v)}
        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)

    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=5e-4)
    train_scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=MILESTONES, gamma=0.2) #learning rate decay
    train_iter_per_epoch = len(train_loader)
    val_iter_per_epoch = len(test_loader)
    print("train: ", train_iter_per_epoch*batch_size)
    print("val: ", val_iter_per_epoch*batch_size)

    # create checkpoint folder to save model
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)
    checkpoint_path = os.path.join(checkpoint_path, '{net}-Epoch:{epoch}-Tloss:{train_loss}-Vloss:{val_loss}-Vacc:{val_acc}.pth')


    for epoch in range(1, Epoch + 1):
        train_loss = 0
        train_lr = 0
        model.train()
        print('Start Train')
        with tqdm(total=train_iter_per_epoch, desc=f'Epoch {epoch}/{Epoch}',postfix=dict,mininterval=0.3) as pbar:
            for iteration, batch in enumerate(train_loader):
                if iteration >= train_iter_per_epoch:
                    break
                images, labels = batch[0], batch[1]
                images *= 255   # 保证输入为整形
                images -= 128
                if gpu:
                    labels = labels.cuda()
                    images = images.cuda()
                optimizer.zero_grad()
                outputs = model(images)
                outputs = torch.squeeze(outputs)
                loss = loss_function(outputs, labels)
                loss.backward()
                optimizer.step()

                train_loss += loss.item()
            
                pbar.set_postfix(**{'loss'  : train_loss / (iteration + 1)})
                pbar.update(1)
        
        val_loss = 0
        val_correct = 0
        val_sum = 0
        val_accuracy = 0
        model.eval()
        print('Start Val')
        with tqdm(total=val_iter_per_epoch, desc=f'Epoch {epoch}/{Epoch}',postfix=dict,mininterval=0.3) as pbar:
            for iteration, batch in enumerate(test_loader):
                if iteration >= val_iter_per_epoch:
                    break
                images, labels = batch[0], batch[1]
                images *= 255   # 保证输入为整形
                images -= 128
                with torch.no_grad():
                    if gpu:
                        labels = labels.cuda()
                        images = images.cuda()
                    optimizer.zero_grad()
                    outputs = model(images)
                    outputs = torch.squeeze(outputs)
                    loss = loss_function(outputs, labels)
                    # 计算准确率
                    _, predicted = torch.max(outputs, 1)
                    c = (predicted == labels).squeeze().sum()
                    val_correct += c
                    val_sum += labels.shape[0]
                    val_accuracy = (val_correct / val_sum).item()

                val_loss += loss.item()

                pbar.set_postfix(**{'loss'  : val_loss / (iteration + 1), 
                                    'acc'   : val_accuracy})
                pbar.update(1)

        torch.save(model.state_dict(), checkpoint_path.format(net=net_name, 
                                                              epoch=epoch, 
                                                              train_loss=round(train_loss/train_iter_per_epoch, 4), 
                                                              val_loss=round(val_loss/val_iter_per_epoch, 4), 
                                                              val_acc=round(val_accuracy, 3)))
