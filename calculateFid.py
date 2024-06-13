import os
import json
from PIL import Image, ImageFile, UnidentifiedImageError
import torchvision.transforms as transforms
from pytorch_fid import fid_score
from tqdm import tqdm
import argparse
import logging

# Allow loading of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Set up logging
logging.basicConfig(filename='image_processing.log', level=logging.DEBUG)

def resize_and_save_image(image, file_path, size):
    """Resize the image to the specified size and save it back to the file path."""
    transform = transforms.Resize(size)
    image = transform(image)
    image.save(file_path)

def resize_images_in_folder(folder_path, size=(480, 360)):
    """Resize all images in the specified folder to the given size."""
    for root, _, files in os.walk(folder_path):
        for filename in tqdm(files):
            if filename.endswith(".png"):
                file_path = os.path.join(root, filename)
                try:
                    with Image.open(file_path) as image:
                        resize_and_save_image(image, file_path, size)
                        logging.debug(f"Resized image: {file_path}")
                except (OSError, UnidentifiedImageError) as e:
                    logging.error(f"Error processing {file_path}: {e}")
                    print(f"Error processing {file_path}: {e}")
                    os.remove(file_path)  # Remove the corrupted image

def filter_images_by_size(folder_path, size):
    """Return a list of image paths that match the specified size."""
    valid_images = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".png"):
                file_path = os.path.join(root, filename)
                try:
                    with Image.open(file_path) as image:
                        if image.size == size:
                            valid_images.append(file_path)
                        else:
                            logging.error(f"Skipping {file_path} due to incorrect size: {image.size}")
                except (OSError, UnidentifiedImageError) as e:
                    logging.error(f"Error processing {file_path}: {e}")
    return valid_images

def calculate_fid_for_all_subfolders(original_folder, transformed_base_folder, output_json_path, size=(480, 360)):
    """Calculate FID scores for each subfolder in the transformed base folder against the original folder."""
    fid_scores = {}

    # Resize images in the original dataset
    print("Resizing original dataset images...")
    logging.debug("Resizing original dataset images...")
    resize_images_in_folder(original_folder, size)

    # Process each subfolder in the transformed base folder
    for subfolder in os.listdir(transformed_base_folder):
        subfolder_path = os.path.join(transformed_base_folder, subfolder)
        if os.path.isdir(subfolder_path):
            print(f"Processing {subfolder}...")
            logging.debug(f"Processing {subfolder}...")

            # Resize images in the transformed subfolder
            resize_images_in_folder(subfolder_path, size)

            

            # Calculate FID score
            try:
                fid_value = fid_score.calculate_fid_given_paths(
                    [original_folder, subfolder_path],
                    batch_size=50,
                    device="cpu",  # Use "cuda" for GPU
                    dims=2048
                ) 
                fid_scores[subfolder] = fid_value
                logging.debug(f"FID score for {subfolder_path}: {fid_value}")
            except Exception as e:
                logging.error(f"Error calculating FID for {subfolder_path}: {e}")
                print(f"Error calculating FID for {subfolder_path}: {e}")

    # Save FID scores to JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(fid_scores, json_file, indent=4)
        logging.debug(f"FID scores saved to {output_json_path}")

def main():
    parser = argparse.ArgumentParser(description="Resize images and calculate FID scores.")
    parser.add_argument("--o", type=str, required=True, help="Path to the original base images folder.")
    parser.add_argument("--t", type=str, required=True, help="Path to the base folder containing transformed subfolders.")
    parser.add_argument("--output", type=str, required=True, help="Path to save the FID scores JSON file.")
    parser.add_argument("--width", type=int, default=480, help="Width to resize images to (default: 480).")
    parser.add_argument("--height", type=int, default=360, help="Height to resize images to (default: 360).")
    
    args = parser.parse_args()
    
    print(f"Starting FID calculation with the following parameters:\n"
          f"Original folder: {args.o}\n"
          f"Transformed folder: {args.t}\n"
          f"Output JSON path: {args.output}\n"
          f"Image size: {args.width}x{args.height}")
    logging.debug(f"Starting FID calculation with the following parameters:\n"
                  f"Original folder: {args.o}\n"
                  f"Transformed folder: {args.t}\n"
                  f"Output JSON path: {args.output}\n"
                  f"Image size: {args.width}x{args.height}")
    
    calculate_fid_for_all_subfolders(args.o, args.t, args.output, size=(args.width, args.height))

if __name__ == "__main__":
    main()
