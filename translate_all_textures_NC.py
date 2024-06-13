import os
import cv2
import json
import argparse
import numpy as np
from tqdm import tqdm
from utils.utils import get_mask
from utils.image_folder import make_dataset

class TranslateTexture(object):
    def __init__(self, black_border=False, random_crop=False, random_flip=True):
        self.texture_dir = json.load(open("/home/dasec/Desktop/FID_final_version/cfg.json"))["texture_sources"]
        self.sources = list(self.texture_dir.keys())
        self.black_border = black_border
        self.random_crop = random_crop
        self.random_flip = random_flip
        self.current_source = None

    def set_source(self, source):
        if source in self.sources:
            self.current_source = source
            self.Textures = make_dataset(self.texture_dir[source])
            self.source = source  # Aktualisiere self.source
        else:
            raise ValueError("Invalid source provided. Available sources are: {}".format(self.sources))
        self.Nt = len(self.Textures)
        print("Set source to {}, Number of textures: {}".format(source, self.Nt))

    def set_augmentation(self, random_crop=False, random_flip=True):
        self.random_crop = random_crop
        self.random_flip = random_flip
        return

    def texture_image(self, image, n=None):
        # Read texture
        if n is None:
            n = np.random.randint(self.Nt)
        texture = cv2.imread(self.Textures[n])
        if texture is None:
            print("Error reading texture: {}".format(self.Textures[n]))
            return None

        # Get image shapes
        H1, W1, _ = texture.shape
        H2, W2, _ = image.shape
        print("Image shape: {}, Texture shape: {}".format(image.shape, texture.shape))

        if self.random_crop:
            # Random Crop
            x = np.random.randint(low=0, high=int((W1 / 3)))
            y = np.random.randint(low=0, high=int((H1 / 3)))
            Wx = W1 - x
            Wy = int((H1 - y) * W2 / H2)
            max_W = min([Wx, Wy])
            W3 = np.random.randint(low=int(0.67 * max_W), high=max_W)
            H3 = int(W3 * H2 / W2)
            rect = [x, y, W3 - 1, H3 - 1]
        else:
            # Max area crop
            W3 = int(W2 * H1 / H2)
            H3 = int(H2 * W1 / W2)
            if H3 < H1:
                y = np.random.randint(low=0, high=H1 - H3)
                rect = [0, y, W1 - 1, H3 - 1]
                x, y, W3, H3 = rect
            elif W3 < W1:
                x = np.random.randint(low=0, high=W1 - W3)
                rect = [x, 0, W3 - 1, H1 - 1]
            else:
                rect = [0, 0, W1 - 1, H1 - 1]

        # Crop texture image
        x, y, W3, H3 = rect
        texture = texture[y : y + H3, x : x + W3]

        # Resize texture
        texture = cv2.resize(texture, (W2, H2), interpolation=cv2.INTER_NEAREST)

        # Random flip
        if self.random_flip:
            if np.random.rand() < 0.5:
                texture = cv2.flip(texture, 0)
            if np.random.rand() < 0.5:
                texture = cv2.flip(texture, 1)

        # Translate texture
        im_out = image.astype(np.int32) + texture.astype(np.int32) - 128

        # Check for saturation
        if im_out.max() > 255:
            im_out = 250 * (im_out - 5) / im_out.max() + 5

        if self.black_border:
            # Find segmentation mask
            mask = get_mask(image)
            # Remove mask
            im_out[mask > 0] = 0

        # Clip image
        np.clip(im_out, 0, 255, out=im_out)

        return im_out

    def texture_folder(self, input_dir, output_dir, exten=".png"):
        # Output Folder
        if output_dir[-1] != "/":
            output_dir = output_dir + "/"

        # Find image names
        Files = make_dataset(input_dir)
        Nf = len(Files)

        print("Processing {} files from {}".format(Nf, input_dir))

        # Loop through all sources
        for source in self.sources:
            # Set the current source
            self.set_source(source)
            
            # Output folder for the current source
            output_dir2 = output_dir + source + "/"
            if not os.path.exists(output_dir2):
                os.makedirs(output_dir2)

            # Loop through all images
            for f in tqdm(range(Nf), desc="Texturing {}".format(source)):
                # File names
                file_in = Files[f]
                file_out = output_dir2 + os.path.basename(file_in)  # Keep the same filename
                
                # Skip hidden files
                if file_in.startswith("._"):
                    print("Skipping hidden file: {}".format(file_in))
                    continue

                # Read image
                image = cv2.imread(file_in)
                if image is None:
                    print("Error reading image: {}".format(file_in))
                    continue

                # Apply texture only for the specified source
                if source in self.texture_dir:
                    # Loop through all textures for the current source
                    for texture_index in range(self.Nt):
                        # Texture image
                        im_out = self.texture_image(image, n=texture_index)
                        if im_out is None:
                            print("Skipping image {} due to texture read error.".format(file_in))
                            continue

                        # Save image with texture applied
                        texture_file_out = file_out[:-len(exten)] + "_texture{}".format(texture_index) + exten
                        cv2.imwrite(texture_file_out, im_out)
                        print("Saved textured image: {}".format(texture_file_out))
                else:
                    # Save the image without texture
                    cv2.imwrite(file_out, image)
                    print("Saved original image without texture: {}".format(file_out))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", default="/home/dasec/Desktop/manual-textures-main/database_example", help="Input path (directly to images)")
    parser.add_argument("-o", "--output_dir", default="/home/dasec/Desktop/manual-textures-main/database_example_test_final", help="Output folder where the classes will be placed")
    parser.add_argument("-b", "--black_border", action="store_true", help="Whether the image has a segmentation black border not to be textured")
    parser.add_argument("-c", "--random_crop", action="store_true", help="Performs texture random crop with the same aspect ratio as the input")
    parser.add_argument("-f", "--random_flip", action="store_true", help="Performs texture random flip (horizontal and vertical)")
    parser.add_argument("-e", "--extension", default=".png", help="Output image extension/format")
    args = parser.parse_args()

    TT = TranslateTexture(black_border=args.black_border, random_crop=args.random_crop, random_flip=args.random_flip)
    
    for source in TT.sources:
        TT.set_source(source)
        TT.texture_folder(input_dir=args.input_dir, output_dir=args.output_dir, exten=args.extension)

    print("Done!\n")
