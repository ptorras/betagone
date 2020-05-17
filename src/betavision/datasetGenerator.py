import Vision as v
import cv2
import glob
import os, shutil
import time

pieces = 'bknpqr'

board = cv2.imread('../../datasets/pieces-full/empty.png')
path_dataset = '../../datasets/pieces/'
path_images = '../../datasets/pieces-full/'

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

def cutndsave(img, num, piece, color, path):

    if color=='w':
        pi = str.upper(piece)
    elif color == 'b':
        pi = piece
    else:
        pi = piece
        color = ''

    boxes = p.cut_boxes(img)

    for i, box in enumerate(boxes):
        imname = path+'/'+pi+color+'_'+str('{0:04}'.format(num+i))+'.png'
        cv2.imwrite(imname,box)

def generateDataset():
    for piece in pieces:
        num = 0
        path2saveim = path_dataset+piece
        file_path_white = str.lower(path_images+piece+'w*.png')
        file_path_black = str.lower(path_images+piece+'b*.png')

        for file in glob.glob(file_path_black):
            im = cv2.imread(file)
            cutndsave(im, num, piece, 'b',path2saveim)
            num += 64

        for file in glob.glob(file_path_white):
            im = cv2.imread(file)
            cutndsave(im, num, piece, 'w',path2saveim)
            num += 64

    cutndsave(board, 0, 'b', None,'../../datasets/pieces/board')

#TODO: add arguments ?????? idk

def main():

    if wipe:
        wipeAllData()

    start = time.time()
    generateDataset()
    end = time.time()

    print('Elapsed time:',str(round((end-start),2))+'s')

if __name__ == '__main__':
    main()