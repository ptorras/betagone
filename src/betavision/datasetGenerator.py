import Vision as v
import cv2
import glob
import os, shutil
import time

black_pieces = 'bknpqr'
white_pieces = 'BKNPQR'

board = cv2.imread('../betatest/tests/empty.png')
path_dataset = './dataset/'
path_images = '../betatest/tests/'

wipe=True

p = v.PieceDetector(board)

def wipeAllData():
    folders = ['b', 'board', 'k', 'n', 'p', 'q', 'r']
    for piece in folders:
        folder = path_dataset+piece
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

def cutndsave(img,num,piece,path):
    boxes = p.cut_boxes(img)
    for i, box in enumerate(boxes):
        imname = path+'/'+piece+str(num+i)+'.png'
        cv2.imwrite(imname,box)

def generateDataset():
    for black_piece, white_piece in zip(black_pieces,white_pieces):
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
    cutndsave(board, 0, 'b', './dataset/board')

def main():

    if wipe:
        wipeAllData()

    start = time.time()
    generateDataset()
    end = time.time()

    print('Time elapsed:',str(round((end-start),2))+'s')

if __name__ == '__main__':
    main()