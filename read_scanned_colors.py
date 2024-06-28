import os
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm
from utils.utils import write_txt
from utils.image_folder import make_dataset

from joblib import Parallel, delayed
from argparse import ArgumentParser as argparse


# Process one page
def process_page(path):
    # Make QR reader object
    QRreader = cv2.QRCodeDetector()

    #Get page ID
    in_ID = path.split('/')[-1].split('.')[0]

    # Read image
    im1 = Image.open(path).convert('RGB')
    W, H = im1.size

    # Get Scale
    scale = (500/W + 712.5/H)/2
    newsize = (int(W*scale), int(H*scale))

    # Scale image
    im2 = np.array(im1.resize(newsize), dtype='uint8')

    # Split in R G B channels
    R = im2[:,:,0]
    G = im2[:,:,1]
    B = im2[:,:,2]

    # Binaryze Image
    bw1 = np.logical_or(R<255, G<255)
    bw1 = np.logical_or( bw1 , B<255)

    # Apply morphological erosion
    bw2 = cv2.erode(bw1.astype('uint8'), se, iterations=2)

    # Get connected components of high area
    N, labeled, stats, centroids = cv2.connectedComponentsWithStats(bw2, connectivity=8)
    areas = np.array(stats[:, cv2.CC_STAT_AREA])
    ind = np.where(np.logical_and(areas>7000 , areas<10000))[0]

    # Get color Bounding Boxes
    left = np.array(stats[ind, cv2.CC_STAT_LEFT])
    top = np.array(stats[ind, cv2.CC_STAT_TOP])
    width = np.array(stats[ind, cv2.CC_STAT_WIDTH])
    height = np.array(stats[ind, cv2.CC_STAT_HEIGHT])
    bb_color = np.array([left, top, left+width, top+height]).T

    # Get QR bounding boxes
    bb_qr = bb_color - [50, 12, 0, 0]
    bb_qr[:,2] = bb_qr[:,0] + 56
    bb_qr[:,3] = bb_qr[:,1] + 56

    # Scale bounding boxes
    bb_color = bb_color/scale
    bb_color = bb_color.astype(int)
    bb_qr = bb_qr/scale
    bb_qr = bb_qr.astype(int)

    # Save all images
    wrong = 0
    for i in range(len(ind)):

        # Crop color and QR
        color = im1.crop(bb_color[i])
        qr = np.array(im1.crop(bb_qr[i]), dtype='uint8')

        # Read QR Code
        qr_value, points, straight_qr = QRreader.detectAndDecode(qr)
        if qr_value == '':
            wrong += 1
            qr_value = 'unknown{:02d}'.format(wrong)
            qr_not_read.append(' - Coords: {} in Page: {} ({})'.format(bb_qr[i], path.split('/')[-1], qr_value))

        # Make output name
        name = "{}_{}.png".format(qr_value.split('.')[0] , in_ID)
        opt_path = os.path.join(args.out_dataset , name)
        color.save(opt_path)


if __name__ == '__main__':
    # Parse arguments
    parser = argparse()
    parser.add_argument('-i', '--in_dataset', default='/home/dasec/Desktop/Transfer-texture/BROTHER-texture',
                                            help='Folder with scanned pages in image format i.e.: .png, .jpg, .bmp, etc.')
    parser.add_argument('-o', '--out_dataset', default='/home/dasec/Desktop/Transfer-texture/Brother-texture-scanned',
                                            help='Output dataset folder to save isolated colors.')
    parser.add_argument('-j', '--jobs', type=int, default=4,
                                            help='Number of parallel jobs')
    args = parser.parse_args()

    # Read pages of scanned colors
    in_dataset = make_dataset(args.in_dataset)
    print('Reading colors from {:d} pages'.format(len(in_dataset)))

    # Make output folder
    if not os.path.exists(args.out_dataset):
        os.makedirs(args.out_dataset)

    # Load structuring element (kernel for morphological operations)
    se = np.load('./utils/se_5x5.npy').astype('uint8')

    # To store not read qr codes
    qr_not_read = []

    # Process all pages
    Parallel(n_jobs=args.jobs)(
        delayed(process_page)(path)
        for path in tqdm(in_dataset, desc='Detecting Colors')
    )

    # Show problematic images
    print(' ')
    if len(qr_not_read) > 0:
        qr_not_read = ['QR not read at:'] + qr_not_read
        for nor_read in qr_not_read:
            print(nor_read)
        write_txt(qr_not_read, 'problematic_qr.txt')
