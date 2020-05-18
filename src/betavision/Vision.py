import cv2
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
from collections import OrderedDict
from BetaNeural import process_image
from PIL import Image
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models


class PieceDetector:
    def __init__(self, board_image:np.ndarray, chkp: str):
        self._board = board_image
        self._points, self._step = self.__getCorners()

        self.model = models.vgg16()
        self.checkpoint = torch.load(chkp)
        #self.model.load_state_dict(self.checkpoint['model_state_dict'])
        #self.model.eval()
        self.__load_checkpoint()

    def __load_checkpoint(self):

        if self.checkpoint['arch'] == 'vgg16':

            self.model = models.vgg16(pretrained=True)

            for param in self.model.parameters():
                param.requires_grad = False
        else:
            print("Architecture not recognized.")

        self.model.class_to_idx = self.checkpoint['class_to_idx']

        classifier = nn.Sequential(OrderedDict([('fc1', nn.Linear(25088, 4096)),
                                                ('relu', nn.ReLU()),
                                                ('drop', nn.Dropout(p=0.5)),
                                                ('fc2', nn.Linear(4096, 13)),
                                                ('output', nn.LogSoftmax(dim=1))]))

        self.model.classifier = classifier

        self.model.load_state_dict(self.checkpoint['model_state_dict'])

    def __getCorners(self):

        g = self._board[:,:,1]
        r = self._board[:,:,2]

        ret1, thresh1 = cv2.threshold(r, 73, 255, cv2.THRESH_BINARY_INV)
        ret2, thresh2 = cv2.threshold(g, 54, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((100,100))

        red = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
        green = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernel)

        ret1, thresh1 = cv2.threshold(red, 73, 255, cv2.THRESH_BINARY_INV)
        ret2, thresh2 = cv2.threshold(green, 54, 255, cv2.THRESH_BINARY_INV)

        edges1 = cv2.Canny(thresh1, 0, 255, apertureSize=3)
        edges2 = cv2.Canny(thresh2, 0, 255, apertureSize=3)

        edges = edges1 + edges2

        minLineLength = 100
        lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=127, lines=np.array([]),
                                minLineLength=minLineLength, maxLineGap=80)

        [minX1, minY1] = [np.amin(lines[:, :, 0]), np.amin(lines[:, :, 1])]
        [minX2, minY2] = [np.amin(lines[:, :, 2]), np.amin(lines[:, :, 3])]
        [maxX1, maxY1] = [np.amax(lines[:, :, 0]), np.amax(lines[:, :, 1])]
        [maxX2, maxY2] = [np.amax(lines[:, :, 2]), np.amax(lines[:, :, 3])]

        A = (min(minX1, minX2), min(minY1, minY2))
        B = (max(maxX1, maxX2), max(maxY1, maxY2))
        C = (B[0], A[1])
        dst = distance.euclidean(A, C)
        step = int(dst / 8)

        return [A, B], step

    def cut_boxes(self, img):

        boxes = list()

        tlc = self._points[0]
        c = 0   # correcció per si les imatges queden mal retallades
        dim = (133,133) # dimensió resize perquè totes les imatges quedin igual de retallades.

        for i in range(0,8):
            y1 = tlc[1] + (i*self._step)
            y2 = y1 + self._step+c

            for j in range(0,8):
                x1 = tlc[0] + (j*self._step)
                x2 = x1 + self._step+c

                casella = img[y1:y2, x1:x2]
                casella = cv2.resize(casella, dim)
                boxes.append(casella)
                # cv2.imshow('casella', casella)
                # cv2.waitKey()
        # cv2.destroyAllWindows()

        return np.asarray(boxes)

    def detect_pieces(self, actual_board:np.ndarray) -> str:
        boxes = self.cut_boxes(actual_board)

        for i, box in enumerate(boxes):
            image_path = '../../datasets/data4neural/test/box_0'+str(i)+'.png'
            cv2.imwrite(image_path, box)
            pil_image = Image.open(image_path)
            top_probabilities, top_classes = self.predict(pil_image)
            print(top_classes[0])

    def predict(self, pil_image, topk=5):
        ''' Predict the class (or classes) of an image using a trained deep learning model.
        '''

        image = process_image(pil_image)

        # Convert image to PyTorch tensor first
        image = torch.from_numpy(image).type(torch.FloatTensor)
        # print(image.shape)
        # print(type(image))

        # Returns a new tensor with a dimension of size one inserted at the specified position.
        image = image.unsqueeze(0)

        output = self.model.forward(image)

        probabilities = torch.exp(output)

        # Probabilities and the indices of those probabilities corresponding to the classes
        top_probabilities, top_indices = probabilities.topk(topk)

        # Convert to lists
        top_probabilities = top_probabilities.detach().type(torch.FloatTensor).numpy().tolist()[0]
        top_indices = top_indices.detach().type(torch.FloatTensor).numpy().tolist()[0]

        # Convert topk_indices to the actual class labels using class_to_idx
        # Invert the dictionary so you get a mapping from index to class.

        idx_to_class = {value: key for key, value in self.model.class_to_idx.items()}
        # print(idx_to_class)

        top_classes = [idx_to_class[index] for index in top_indices]

        return top_probabilities, top_classes

#---- PROVES ---- ELIMINAR QUAN LA CLASSE ESTIGUI ACABADA.
def main():
    #Exemple de com funciona:
    board = cv2.imread("./testpic/taulell.png")
    actual_board = cv2.imread("../../datasets/early-test/00001_post.png")
    p = PieceDetector(board,'./checkpoint-100v2.pth')
    p.detect_pieces(actual_board)


if __name__ == "__main__":
    main()