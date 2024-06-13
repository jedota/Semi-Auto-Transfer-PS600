import os
from PIL import Image
import torchvision.transforms as transforms
import argparse

def convert_to_png(image_path):
    """Konvertiert das Bild in das PNG-Format."""
    try:
        image = Image.open(image_path)
        png_path = os.path.splitext(image_path)[0] + ".png"
        image.save(png_path, "PNG")
        os.remove(image_path)
        print(f"Konvertiert: {image_path} zu {png_path}")
        return png_path
    except Exception as e:
        print(f"Fehler bei der Konvertierung von {image_path}: {e}")
        return None

def resize_images_in_folder(folder_path, size=(480, 360)):
    """Passt die Größe aller Bilder im Verzeichnis an und konvertiert JPG-Bilder in PNG."""
    transform = transforms.Resize(size)
    
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                if not file_path.endswith(".png"):
                    # Konvertieren von JPG nach PNG
                    if file_path.lower().endswith(".jpg") or file_path.lower().endswith(".jpeg"):
                        file_path = convert_to_png(file_path)
                        if file_path is None:
                            continue

                with Image.open(file_path) as image:
                    image = transform(image)
                    image.save(file_path)
                    print(f"Größe angepasst: {file_path}")
            except Exception as e:
                print(f"Fehler beim Verarbeiten von {file_path}: {e}")

# Argumente parsen
parser = argparse.ArgumentParser(description="Transformiere Bilder im Verzeichnis mit neuen Dimensionen.")
parser.add_argument("--directory", "-d", required=True, help="Pfad zum Verzeichnis mit den Bildern")
args = parser.parse_args()

print(f"Starte Verarbeitung des Verzeichnisses: {args.directory}")
# Bilder im angegebenen Verzeichnis und dessen Unterverzeichnissen laden und transformieren
resize_images_in_folder(args.directory)

print(f"Alle Bilder im Verzeichnis {args.directory} und dessen Unterverzeichnissen wurden transformiert.")
