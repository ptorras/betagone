import Vision as v
import cv2
import glob
import os, shutil
import time

N = (11*2*64)
Nb = 64
t_test = 0.2
t_val = 0.2
t_train = 0.6

pieces = 'bknpqr'

board = cv2.imread('../../datasets/pieces-full/empty.png')
path_dataset = '../../datasets/pieces/'
path_images = '../../datasets/data4neuralv2/images/'

wipe=False

p = v.PieceDetector(board, './checkpoint-100.pth')

def generateFolders(path):
    folders = ['train', 'test', 'val']
    for folder in folders:
        path_board = path +'/' +folder + '/board'
        os.mkdir(path_board)
        for piece in pieces:
            path_total_white = path + '/' + folder + '/' + piece+ 'w'
            path_total_black = path + '/' + folder + '/' + piece+ 'b'
            os.mkdir(path_total_white)
            os.mkdir(path_total_black)


def wipeAllData(folder):
    if folder ==  'pieces':
        folders = ['b', 'board', 'k', 'n', 'p', 'q', 'r']
        path = path_dataset
    elif folder == 'data4neural':
        path = '../../datasets/data4neural/'
        folders = ['train', 'test', 'val']

    for piece in folders:
        folder = path+piece
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
        im_name = path+'/'+pi+color+'_'+str('{0:04}'.format(num+i))+'.png'
        cv2.imwrite(im_name,box)

def cutndsave_v2(img, num, piece, color, path):

    if color=='w':
        pi = str.upper(piece)
        X = N
    elif color == 'b':
        pi = piece
        X = N
    else:
        pi = piece
        color = ''
        X = Nb

    boxes = p.cut_boxes(img)

    for i, box in enumerate(boxes):
        n = num + i

        # if n < (X*t_train):
        #     folder = '/train/'
        # elif n > (X*t_train) and n < (X*t_train + X*t_test):
        #     folder = '/test/'
        # elif n > (X*t_train + X*t_test) and n < X:
        #     folder = '/val/'

        im_name = path + '/' + str.lower(pi) +'/'+ pi + color + '_' + str('{0:04}'.format(n)) + '.png'
        cv2.imwrite(im_name,box)

def generateDataset_v2():
    for piece in pieces:
        num_black = 0
        num_white = 0
        path2saveim = '../../datasets/pieces'
        file_path_white = str.lower(path_images+piece+'w*.png')
        file_path_black = str.lower(path_images+piece+'b*.png')

        for file in glob.glob(file_path_black):
            im = cv2.imread(file)
            cutndsave_v2(im, num_black, piece, 'b',path2saveim)
            num_black += 64

        for file in glob.glob(file_path_white):
            im = cv2.imread(file)
            cutndsave_v2(im, num_white, piece, 'w',path2saveim)
            num_white += 64

    cutndsave_v2(board, 0, 'b', None,'../../datasets/pieces')

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

    cutndsave(board, 0, 'board', None,'../../datasets/pieces/board')

#TODO: add arguments ?????? idk

def main():

    if wipe:
        wipeAllData('pieces')
        #generateFolders('../../datasets/data4neural')


    start = time.time()
    #generateDataset()
    generateDataset_v2()
    end = time.time()

    print('Elapsed time:',str(round((end-start),2))+'s')

    files = os.listdir('../../datasets/data4neural/train')
    print('Files train:', len(files))
    files = os.listdir('../../datasets/data4neural/test')
    print('Files test:', len(files))
    files = os.listdir('../../datasets/data4neural/val')
    print('Files val:', len(files))

if __name__ == '__main__':
    main()