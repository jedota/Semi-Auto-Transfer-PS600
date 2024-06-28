import os
import numpy as np
from PIL import Image
from tqdm import tqdm
from utils.utils import write_txt
from utils.image_folder import make_dataset

from joblib import Parallel, delayed
from argparse import ArgumentParser as argparse

# Process a single color
def process_color(path):
    # Make I/O names
    name = path.split('/')[-1]
    original_color = name[:7]
    out_path = os.path.join(args.out_dataset , name)

    if original_color!='unknown' or args.method=='mean':
        # Read color image
        color = Image.open(path).convert('RGB')
        W, H = color.size

        # Convert to numpy
        color_np = np.array(color, dtype='float')/255

        # Get main color
        if args.method=='QR':
            org_color_path = './original_colors/{}.npy'.format(original_color)
            RGB = np.load(org_color_path).astype(float)
            R = RGB[0]/255
            G = RGB[1]/255
            B = RGB[2]/255
        elif args.method=='mean':
            R = np.average(color_np[:,:,0])
            G = np.average(color_np[:,:,1])
            B = np.average(color_np[:,:,2])
        main_color = np.concatenate((
            R*np.ones((H, W, 1), dtype='float'),
            G*np.ones((H, W, 1), dtype='float'),
            B*np.ones((H, W, 1), dtype='float')
        ), axis=2)

        # Subtract main color
        texture = color_np - main_color + 0.5
        texture = np.clip(255*texture, 0, 255).astype('uint8')

        # Save texture
        texture = Image.fromarray(texture).convert('RGB')
        texture.save(out_path)


if __name__ == '__main__':
    # Parse arguments
    parser = argparse()
    parser.add_argument('-i', '--in_dataset', default='/home/dasec/Desktop/Transfer-texture/Brother-texture-scanned',
                                            help='Folder with images of textured colors.')
    parser.add_argument('-o', '--out_dataset', default='/home/dasec/Desktop/Transfer-texture/B600_scanned_isolated',
                                            help='Output dataset folder to save isolated textures.')
    parser.add_argument('-m', '--method', default='QR',
                                            help='Method for subtracting the main color: < QR | mean >')
    parser.add_argument('-j', '--jobs', type=int, default=4,
                                            help='Number of parallel jobs')
    args = parser.parse_args()

    # Read all colors
    color_dataset = make_dataset(args.in_dataset)
    print('Procesing {} textured colors'.format(len(color_dataset)))

    # Make output folder
    if not os.path.exists(args.out_dataset):
        os.makedirs(args.out_dataset)

    # Process all colors
    Parallel(n_jobs=args.jobs)(
        delayed(process_color)(path)
        for path in tqdm(color_dataset, desc='Isolating textures')
    )
    print(' ')
