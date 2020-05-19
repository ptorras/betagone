from sklearn.model_selection import train_test_split
from collections import OrderedDict
import numpy as np
import time as t
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from PIL import Image
import cv2
import glob

import torch
import ctypes
ctypes.cdll.LoadLibrary('caffe2_nvrtc.dll')
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models

pieces = 'bknpqr'
colors = 'bw'
board = 'board'

dataset_folder = '../../datasets/data4neural'
train_dir = dataset_folder+'/train'
test_dir = dataset_folder+'/test'
val_dir = dataset_folder+'/val'

def load_piece_dataset(pieces):
    data = list()

    for piece in pieces:
        path = str.lower(dataset_folder + piece + '/' + piece + '*.png')
        for file in glob.glob(path):
            im = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            data.append(im)

    path = str.lower(dataset_folder + board + '/*.png')

    for file in glob.glob(path):
        im = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        data.append(im)

    data = np.asarray(data)

    training_nd_validation, testing_dataset = train_test_split(data, shuffle=True)
    training_dataset, validation_dataset = train_test_split(training_nd_validation, shuffle=True)
    train_loader = torch.utils.data.DataLoader(training_dataset, batch_size=64, shuffle=True)
    test_loader = torch.utils.data.DataLoader(testing_dataset, batch_size=32)
    validate_loader = torch.utils.data.DataLoader(validation_dataset, batch_size=32)

    return train_loader, test_loader, validate_loader

def load_piece_dataset_v2():
    training_transforms = transforms.Compose([transforms.ToTensor(),
                                              transforms.Normalize([0.485, 0.456, 0.406],
                                                                   [0.229, 0.224, 0.225])])

    validation_transforms = transforms.Compose([transforms.ToTensor(),
                                                transforms.Normalize([0.485, 0.456, 0.406],
                                                                     [0.229, 0.224, 0.225])])

    # testing_transforms = transforms.Compose([transforms.Resize(256),
    #                                          transforms.CenterCrop(224),
    #                                          transforms.ToTensor(),
    #                                          transforms.Normalize([0.485, 0.456, 0.406],
    #                                                               [0.229, 0.224, 0.225])])

    training_dataset = datasets.ImageFolder(train_dir, transform=training_transforms)
    validation_dataset = datasets.ImageFolder(val_dir, transform=validation_transforms)
    #testing_dataset = datasets.ImageFolder(test_dir, transform=testing_transforms)

    train_loader = torch.utils.data.DataLoader(training_dataset, batch_size=64, shuffle=True)
    validate_loader = torch.utils.data.DataLoader(validation_dataset, batch_size=32)
    #test_loader = torch.utils.data.DataLoader(testing_dataset, batch_size=32)

    return train_loader, training_dataset, validate_loader #,test_loader

def piece2name(pieces, colors):
    pieces_to_name = dict()
    N = len(pieces)
    x = 0

    for i in range(0,N):
        for j in range(0,2):
            x+=1
            pieces_to_name[x] = pieces[i]+colors[j]

    pieces_to_name[(N*2)+1] = 'board'

    return pieces_to_name

def init_nd_config_model():
    model = models.vgg16(pretrained=True)
    print(model)
    for parameter in model.parameters():
        parameter.requires_grad = False

    classifier = nn.Sequential(OrderedDict([('fc1', nn.Linear(25088, 4096)),
                                            ('relu', nn.ReLU()),
                                            ('drop', nn.Dropout(p=0.5)),
                                            ('fc2', nn.Linear(4096, 13)),
                                            ('output', nn.LogSoftmax(dim=1))]))

    model.classifier = classifier

    return model

def validation(model, validateloader, criterion):
    val_loss = 0
    accuracy = 0

    for images, labels in iter(validateloader):
        images, labels = images.to('cuda:0'), labels.to('cuda:0')

        output = model.forward(images)
        val_loss += criterion(output, labels).item()

        probabilities = torch.exp(output)

        equality = (labels.data == probabilities.max(dim=1)[1])
        accuracy += equality.type(torch.FloatTensor).mean()

    return val_loss, accuracy

def train_classifier(model, optimizer, criterion, train_loader, validate_loader):

    epochs = 25
    steps = 0
    print_every = 40

    model.to('cuda:0')

    for e in range(epochs):

        model.train()

        running_loss = 0

        for images, labels in iter(train_loader):

            steps += 1

            images, labels = images.to('cuda:0'), labels.to('cuda:0')

            optimizer.zero_grad()

            output = model.forward(images)
            loss = criterion(output, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            if steps % print_every == 0:
                model.eval()

                # Turn off gradients for validation, saves memory and computations
                with torch.no_grad():
                    validation_loss, accuracy = validation(model, validate_loader, criterion)

                print("Epoch: {}/{}.. ".format(e + 1, epochs),
                      "Training Loss: {:.3f}.. ".format(running_loss / print_every),
                      "Validation Loss: {:.3f}.. ".format(validation_loss / len(validate_loader)),
                      "Validation Accuracy: {:.3f}".format(accuracy / len(validate_loader)))

                running_loss = 0
                model.train()

def test_accuracy(model, test_loader):
    # Do validation on the test set
    model.eval()
    model.to('cuda:0')

    with torch.no_grad():
        accuracy = 0

        for images, labels in iter(test_loader):
            images, labels = images.to('cuda:0'), labels.to('cuda:0')

            output = model.forward(images)

            probabilities = torch.exp(output)

            equality = (labels.data == probabilities.max(dim=1)[1])

            accuracy += equality.type(torch.FloatTensor).mean()

        print("Test Accuracy: {}".format(accuracy / len(test_loader)))

def save_checkpoint(model, training_dataset):

    model.class_to_idx = training_dataset.class_to_idx

    checkpoint = {'arch': "vgg16",
                  'class_to_idx': model.class_to_idx,
                  'model_state_dict': model.state_dict()
                 }

    torch.save(checkpoint, 'checkpoint-100v2.pth')

def is_cuda_available():
    # setting device on GPU if available, else CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Using device:', device)
    print()

    # Additional Info when using cuda
    if device.type == 'cuda':
        print(torch.cuda.get_device_name(0))
        print('Memory Usage:')
        print('Allocated:', round(torch.cuda.memory_allocated(0) / 1024 ** 3, 1), 'GB')
        print('Cached:   ', round(torch.cuda.memory_cached(0) / 1024 ** 3, 1), 'GB')

def process_image(pil_image):
    ''' Scales, crops, and normalizes a PIL image for a PyTorch model,
        returns an Numpy array
    '''

    # Process a PIL image for use in a PyTorch model

    # # Resize
    # if pil_image.size[0] > pil_image.size[1]:
    #     pil_image.thumbnail((5000, 256))
    # else:
    #     pil_image.thumbnail((256, 5000))
    #
    # # Crop
    # left_margin = (pil_image.width - 224) / 2
    # bottom_margin = (pil_image.height - 224) / 2
    # right_margin = left_margin + 224
    # top_margin = bottom_margin + 224
    #
    # pil_image = pil_image.crop((left_margin, bottom_margin, right_margin, top_margin))

    # Normalize
    np_image = np.array(pil_image) / 255
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    np_image = (np_image - mean) / std

    # PyTorch expects the color channel to be the first dimension but it's the third dimension in the PIL image and Numpy array
    # Color channel needs to be first; retain the order of the other two dimensions.
    np_image = np_image.transpose((2, 0, 1))

    return np_image

def main():
    #LOADING DATASETS
    is_cuda_available()
    train_loader, training_dataset, validate_loader = load_piece_dataset_v2()
    pieces_to_names = piece2name(pieces, colors)

    model = init_nd_config_model()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.classifier.parameters(), lr=0.001, momentum=0.9)

    start = t.time()
    train_classifier(model, optimizer, criterion, train_loader, validate_loader)
    save_checkpoint(model, training_dataset)
    end = t.time()

    time = end - start

    m, s = divmod(time, 60)
    h, m = divmod(m, 60)

    print('{:d}h:{:02d}m:{:02d}s'.format(int(h), int(m), int(s)))

    #test_accuracy(model, test_loader)



if __name__ == '__main__':
    main()

