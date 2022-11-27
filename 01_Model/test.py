import torch
import torchvision
import time

from net import Net_DW

# CIFAR100_TRAIN_MEAN = (0.1307)
# CIFAR100_TRAIN_STD = (0.3081)

if __name__ == "__main__":
    gpu = False
    batch_size = 1
    model_path = "01_Model/models/[Net_DW]-Epoch46-Acc0.921.pth"

    test_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST('00_Data', train=False, download=True,
                                transform=torchvision.transforms.Compose([
                                    torchvision.transforms.ToTensor(),
                                    # torchvision.transforms.Normalize(
                                    #     CIFAR100_TRAIN_MEAN, CIFAR100_TRAIN_STD)
                                ])),
        batch_size=batch_size, shuffle=True)
    
    model = Net_DW()

    if gpu:
        model = model.cuda()

    print('Load weights {}.'.format(model_path))
    device          = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    pretrained_dict = torch.load(model_path, map_location = device)
    model.load_state_dict(pretrained_dict)

    
    test_correct = 0
    test_sum = 0
    test_accuracy = 0
    model.eval()
    t1 = time.time()
    for iteration, batch in enumerate(test_loader):
        images, labels = batch[0], batch[1]
        images *= 255   # 保证输入为整形
        images -= 128
        with torch.no_grad():
            if gpu:
                labels = labels.cuda()
                images = images.cuda()
            outputs = model(images)
            # outputs = torch.squeeze(outputs)  # batch不为1的时候使用
            _, predicted = torch.max(outputs, 1)
            c = (predicted == labels).squeeze().sum()
            test_correct += c
            test_sum += labels.shape[0]
    t2 = time.time()
    
    val_accuracy = (test_correct / test_sum).item()
    print("acc:{:.4f}".format(val_accuracy))
    print("time:{:.6f}".format((t2-t1)/test_sum))
    # print(torch.argmax(torch.squeeze(outputs)).item())