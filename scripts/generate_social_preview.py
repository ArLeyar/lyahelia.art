from PIL import Image
import os
from pathlib import Path

def generate_social_preview(source_image_path):
    root_dir = Path(__file__).parent.parent
    # Open the source image
    img = Image.open(root_dir / source_image_path)
    
    # Calculate the aspect ratio
    target_width = 1200
    target_height = 630
    target_ratio = target_width / target_height
    
    # Get current dimensions
    width, height = img.size
    ratio = width / height
    
    # Calculate dimensions for cropping
    if ratio > target_ratio:
        # Image is wider than needed
        new_width = int(height * target_ratio)
        offset = (width - new_width) // 2
        img = img.crop((offset, 0, offset + new_width, height))
    else:
        # Image is taller than needed
        new_height = int(width / target_ratio)
        offset = (height - new_height) // 2
        img = img.crop((0, offset, width, offset + new_height))
    
    # Resize to target dimensions
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Create social media directory if it doesn't exist
    os.makedirs(root_dir / 'images/social', exist_ok=True)
    
    # Save the image
    img.save(root_dir / 'images/social/preview.jpg', 'JPEG', quality=95)

if __name__ == '__main__':
    generate_social_preview('images/gallery/textures/textures-6.jpg') 