from sklearn.model_selection import train_test_split
from collections import OrderedDict
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import cv2
import glob

import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models


pieces = 'bknpqr'
colors = 'bw'
board = 'board'

dataset_folder = '../../datasets/pieces/'

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

    return np.asarray(data)

def piece2name(pieces,colors):
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
    model = models.alexnet(pretrained=True)
    print(model)
    for parameter in model.parameters():
        parameter.requires_grad = False

    classifier = nn.Sequential(OrderedDict([('fc1', nn.Linear(9216, 4096)),
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
        images, labels = images.to('cuda'), labels.to('cuda')

        output = model.forward(images)
        val_loss += criterion(output, labels).item()

        probabilities = torch.exp(output)

        equality = (labels.data == probabilities.max(dim=1)[1])
        accuracy += equality.type(torch.FloatTensor).mean()

    return val_loss, accuracy


def train_classifier(model, optimizer, criterion, train_loader, validate_loader):

    epochs = 15
    steps = 0
    print_every = 40

    model.to('cuda')

    for e in range(epochs):

        model.train()

        running_loss = 0

        for images, labels in iter(train_loader):

            steps += 1

            images, labels = images.to('cuda'), labels.to('cuda')

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
    model.to('cuda')

    with torch.no_grad():
        accuracy = 0

        for images, labels in iter(test_loader):
            images, labels = images.to('cuda'), labels.to('cuda')

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

    torch.save(checkpoint, 'checkpoint.pth')


def main():
    # LOADING DATASETS
    data = load_piece_dataset(pieces)
    pieces_to_names = piece2name(pieces,colors)
    training_nd_validation, testing_dataset = train_test_split(data, shuffle=True)
    training_dataset, validation_dataset = train_test_split(training_nd_validation, test_size=0.25, shuffle=True)
    train_loader = torch.utils.data.DataLoader(training_dataset, batch_size=64, shuffle=True)
    test_loader = torch.utils.data.DataLoader(testing_dataset, batch_size=32)
    validate_loader = torch.utils.data.DataLoader(validation_dataset, batch_size=32)


    model = init_nd_config_model()
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=0.001)

    train_classifier(model, optimizer, criterion, train_loader, validate_loader)

    test_accuracy(model, test_loader)

    #save_checkpoint(model, training_dataset)



if __name__ == '__main__':
    main()

