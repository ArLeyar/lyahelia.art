from PIL import Image
import os
from pathlib import Path

def create_favicon_dir():
    root_dir = Path(__file__).parent.parent
    os.makedirs(root_dir / 'images/favicons', exist_ok=True)

def generate_favicons(source_image_path):
    root_dir = Path(__file__).parent.parent
    img = Image.open(root_dir / source_image_path)
    
    # Generate ICO file
    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    ico_images = []
    for size in ico_sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        ico_images.append(resized)
    ico_images[0].save(root_dir / 'images/favicons/favicon.ico', format='ICO', sizes=ico_sizes)
    
    # Generate PNG favicons
    sizes = {
        'favicon-16x16.png': (16, 16),
        'favicon-32x32.png': (32, 32),
        'apple-touch-icon.png': (180, 180),
        'android-chrome-192x192.png': (192, 192),
        'android-chrome-512x512.png': (512, 512)
    }
    
    for filename, size in sizes.items():
        resized = img.resize(size, Image.Resampling.LANCZOS)
        resized.save(root_dir / f'images/favicons/{filename}', 'PNG')

if __name__ == '__main__':
    create_favicon_dir()
    generate_favicons('images/gallery/textures/textures-6.jpg') 