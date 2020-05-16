import Vision as v
import cv2
import glob


black_pices = 'bknpqr'
white_pices = 'BKNPQR'

taulell = cv2.imread('../betatest/tests/empty.png')
path_dataset = './dataset/'
path_images = '../betatest/tests/'

p = v.PieceDetector(taulell)



def cutndsave(img,num,piece,path):
    boxes = p.cut_boxes(img)
    for i, box in enumerate(boxes):
        imname = path+'/'+piece+str(num+i)+'.png'
        cv2.imwrite(imname,box)



for black_piece, white_piece in zip(black_pices,white_pices):
    num = 0
    path2saveim = path_dataset+black_piece
    file_path_white = path_images+white_piece+'*.png'
    file_path_black = path_images+black_piece+'*.png'

    for file in glob.glob(file_path_black):
        im = cv2.imread(file)
        cutndsave(im, num, black_piece, path2saveim)
        num += 64

    for file in glob.glob(file_path_white):
        im = cv2.imread(file)
        cutndsave(im, num, white_piece, path2saveim)
        num += 64

cutndsave(taulell,0,'b','./dataset/board')