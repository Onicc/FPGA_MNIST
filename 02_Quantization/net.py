import torch.nn as nn
import torch.nn.functional as F
 
class BaseConv(nn.Module):
    def __init__(self, in_channels, out_channels, ksize, stride, groups=1, bias=False):
        super().__init__()
        pad         = (ksize - 1) // 2
        self.conv   = nn.Conv2d(in_channels, out_channels, kernel_size=ksize, stride=stride, padding=pad, groups=groups, bias=bias)
        self.bn     = nn.BatchNorm2d(out_channels, eps=0.001, momentum=0.03)
        self.act    = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.act(self.bn(self.conv(x)))

class DWConv(nn.Module):
    def __init__(self, in_channels, out_channels, ksize, stride=1):
        super().__init__()
        self.dconv = BaseConv(in_channels, in_channels, ksize=ksize, stride=stride, groups=in_channels)
        self.pconv = BaseConv(in_channels, out_channels, ksize=1, stride=1, groups=1)

    def forward(self, x):
        x = self.dconv(x)
        return self.pconv(x)

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = BaseConv(in_channels=1, out_channels=32, ksize=3, stride=2)
        self.conv2 = BaseConv(in_channels=32, out_channels=32, ksize=3, stride=3)
        self.conv3 = BaseConv(in_channels=32, out_channels=32, ksize=3, stride=3)
        self.conv4 = BaseConv(in_channels=32, out_channels=10, ksize=3, stride=2)

    def forward(self, x):
        x = self.conv1(x)
        # import numpy as np
        # np.set_printoptions(threshold=np.inf)
        # print(np.round(x.cpu().numpy(), 2))
        # print(np.array(x.cpu().numpy()*10, dtype=np.int32))
        x = self.conv2(x)
        # print(np.round(x.cpu().numpy(), 2))
        # print(np.array(x.cpu().numpy()*20, dtype=np.int32))
        x = self.conv3(x)
        x = self.conv4(x)

        return x


class Net_DW(nn.Module):
    def __init__(self):
        super(Net_DW, self).__init__()
        self.conv1 = DWConv(in_channels=1, out_channels=6, ksize=3, stride=2)
        self.conv2 = DWConv(in_channels=6, out_channels=6, ksize=3, stride=3)
        self.conv3 = DWConv(in_channels=6, out_channels=6, ksize=3, stride=3)
        self.conv4 = DWConv(in_channels=6, out_channels=10, ksize=3, stride=2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)

        return x

 
class Net1(nn.Module):
    def __init__(self):
        super(Net1, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)
    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)