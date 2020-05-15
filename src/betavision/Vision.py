import cv2
import numpy as np

class PieceDetector:
    def __init__(self, board_image:np.ndarray):
        self.img = board_image

    def detect_pieces(self) -> str:
        pass
