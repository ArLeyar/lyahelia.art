from PIL import Image
import os
from pathlib import Path

def strip_exif(img):
    """Remove EXIF data to reduce file size and ensure compatibility"""
    data = list(img.getdata())
    image_without_exif = Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    return image_without_exif

def generate_social_preview(source_image_path):
    root_dir = Path(__file__).parent.parent
    # Open the source image
    img = Image.open(root_dir / source_image_path)
    
    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, 'white')
        background.paste(img, mask=img.getchannel('A'))
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Calculate the aspect ratio
    # Telegram prefers 1200x630 or 1.91:1 ratio
    target_width = 1200
    target_height = 630
    target_ratio = target_width / target_height
    
    # Get current dimensions
    width, height = img.size
    ratio = width / height
    
    # Calculate dimensions for padding instead of cropping
    if ratio > target_ratio:
        # Image is wider than target - add padding top/bottom
        new_height = int(width / target_ratio)
        canvas = Image.new('RGB', (width, new_height), 'white')
        offset = (new_height - height) // 2
        canvas.paste(img, (0, offset))
        img = canvas
    else:
        # Image is taller than target - add padding left/right
        new_width = int(height * target_ratio)
        canvas = Image.new('RGB', (new_width, height), 'white')
        offset = (new_width - width) // 2
        canvas.paste(img, (offset, 0))
        img = canvas
    
    # Resize to target dimensions
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Strip EXIF data
    img = strip_exif(img)
    
    # Create social media directory if it doesn't exist
    os.makedirs(root_dir / 'images/social', exist_ok=True)
    
    # Save the main preview image
    # Telegram recommends JPEG with quality between 80-85% and file size < 5MB
    img.save(
        root_dir / 'images/social/preview.jpg',
        'JPEG',
        quality=85,
        optimize=True,
        progressive=True
    )
    
    # Create a smaller version for faster loading and fallback
    small_img = img.resize((600, 315), Image.Resampling.LANCZOS)
    small_img.save(
        root_dir / 'images/social/preview-small.jpg',
        'JPEG',
        quality=85,
        optimize=True,
        progressive=True
    )
    
    # Print image sizes for verification
    main_size = (root_dir / 'images/social/preview.jpg').stat().st_size / 1024  # KB
    small_size = (root_dir / 'images/social/preview-small.jpg').stat().st_size / 1024  # KB
    print(f"Generated preview images:")
    print(f"Main preview: {main_size:.1f}KB")
    print(f"Small preview: {small_size:.1f}KB")

if __name__ == '__main__':
    generate_social_preview('images/Untitled_Artwork.png') 