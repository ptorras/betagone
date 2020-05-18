import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import numpy as np

classes = ('bb', 'bw', 'board', 'kb',
           'kw', 'nb', 'kw', 'nb', 'nw',
           'pb', 'pw', 'qb', 'qw', 'rb', 'rw')

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d()
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d()
        self.

    def forward(self, x):
        pass