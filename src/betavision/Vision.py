import cv2
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt

class PieceDetector:
    def __init__(self, board_image:np.ndarray):
        self._board = board_image
        self._points, self._step = self.__getCorners()

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

    def __cut_boxes(self, img):

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

                cv2.imshow('casella', casella)
                cv2.waitKey()

        cv2.destroyAllWindows()


    def detect_pieces(self, actual_board:np.ndarray) -> str:
        self.__cut_boxes(actual_board)


#---- PROVES ---- ELIMINAR QUAN LA CLASSE ESTIGUI ACABADA.
def main():
    #Exemple de com funciona:
    board = cv2.imread("./testpic/taulell.png")
    actual_board = cv2.imread("./testpic/ze4.png")
    p = PieceDetector(board)
    p.detect_pieces(actual_board)


if __name__ == "__main__":
    main()