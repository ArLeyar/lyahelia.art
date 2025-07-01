from PIL import Image, ImageOps
import os
import re
from pathlib import Path
import pillow_heif

def optimize_image(input_path, output_path, max_width=2400, quality=95):
    """
    Optimize image while preserving high quality for artist portfolio.
    Uses higher resolution limit and quality settings to maintain color fidelity.
    """
    if input_path.suffix.lower() == '.heic':
        heif_file = pillow_heif.read_heif(input_path)
        img = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
    else:
        img = Image.open(input_path)
        # Preserve the orientation from EXIF data
        img = ImageOps.exif_transpose(img)
    
    # Convert RGBA to RGB with white background if needed
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, 'white')
        background.paste(img, mask=img.getchannel('A'))
        img = background
    
    # Only resize if image is significantly larger than max_width
    width, height = img.size
    if width > max_width:
        ratio = max_width / width
        new_size = (max_width, int(height * ratio))
        # Use LANCZOS for high-quality resizing
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Save with high quality settings optimized for art
    img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
    if hasattr(img, 'close'):
        img.close()

def clean_filename(filename):
    """Clean filename and ensure it's lowercase"""
    # Remove file extension for processing
    name_without_ext = Path(filename).stem
    # Replace non-alphanumeric characters with hyphens and make lowercase
    cleaned = re.sub(r'[^a-zA-Z0-9\-\.\(\)\s]', '-', name_without_ext)
    # Replace multiple hyphens with single hyphen
    cleaned = re.sub(r'-+', '-', cleaned)
    # Remove leading/trailing hyphens
    cleaned = cleaned.strip('-')
    return cleaned.lower()

def process_portfolio():
    """Process portfolio images while preserving structure and ensuring lowercase filenames"""
    root_dir = Path(__file__).parent.parent
    portfolio_dir = root_dir / 'images/portfolio'
    
    if not portfolio_dir.exists():
        print(f"Directory not found: {portfolio_dir}")
        return
    
    # Get all subdirectories in portfolio
    subdirs = [d for d in portfolio_dir.iterdir() if d.is_dir()]
    
    for subdir in subdirs:
        print(f"\nProcessing folder: {subdir.name}")
        
        # Get all image files in this subdirectory
        image_files = [f for f in subdir.glob('*') if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.heic', '.JPG')]
        
        for file in image_files:
            # Create lowercase filename
            clean_name = clean_filename(file.name)
            new_filename = f"{clean_name}.jpg"
            final_output = subdir / new_filename
            
            # Skip if filename is already correct
            if file.name.lower() == new_filename and file.suffix.lower() == '.jpg':
                print(f"  Skipping (already optimized): {file.name}")
                continue
            
            # Create a temporary optimized file
            temp_output = subdir / f"{clean_name}.tmp.jpg"
            
            try:
                print(f"  Optimizing: {file.name} -> {new_filename}")
                optimize_image(file, temp_output, max_width=2400, quality=95)
                
                # If original filename is different, remove it
                if file.name != new_filename:
                    file.unlink()
                
                # Rename temp to final filename
                temp_output.rename(final_output)
                
            except Exception as e:
                print(f"  Error processing {file}: {e}")
                # Clean up temp file if it exists
                if temp_output.exists():
                    temp_output.unlink()

def process_lyahelia():
    root_dir = Path(__file__).parent.parent
    lyahelia_dir = root_dir / 'images/lyahelia'
    
    if not lyahelia_dir.exists():
        print(f"Directory not found: {lyahelia_dir}")
        return
    
    # Get all image files and sort them
    image_files = [f for f in lyahelia_dir.glob('*') if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.heic', '.JPG')]
    image_files = sorted(image_files)
    
    # Process each image with numeric naming
    for idx, file in enumerate(image_files, 1):
        # Skip already processed files
        if file.stem.startswith('lyahelia-'):
            continue
            
        output_filename = f"lyahelia-{idx}.jpg"
        output_path = lyahelia_dir / output_filename
        
        # Don't overwrite existing files with the same name
        if output_path.exists():
            print(f"File already exists: {output_path}")
            continue
        
        try:
            print(f"Optimizing: {file.name} -> {output_filename}")
            optimize_image(file, output_path, max_width=2400, quality=95)
            # Note: originals are kept
        except Exception as e:
            print(f"Error processing {file}: {e}")

def process_gallery(folder_name=None):
    root_dir = Path(__file__).parent.parent
    gallery_path = root_dir / 'images/gallery'
    series_info = {
        'textures': [],
        'elements': [],
        'emotional-postcards': [],
        'girl-in-bistro': [],
        'manifesto': []
    }
    
    folders_to_process = [folder_name] if folder_name else series_info.keys()
    
    for series in folders_to_process:
        if series not in series_info:
            series_info[series] = []
            
        series_path = gallery_path / series
        if not series_path.exists():
            continue
            
        for idx, file in enumerate(sorted(series_path.glob('*')), 1):
            if file.suffix.lower() in ('.jpg', '.jpeg', '.png', '.heic', '.JPG'):
                year = '2024'
                title = f"{series.replace('-', ' ').title()} {idx}"
                
                if series == 'textures':
                    match = re.match(r'(\d{4}):([^:]+)', file.name)
                    if match:
                        year = match.group(1)
                        title = match.group(2).replace(':', ' ')
                elif series == 'girl-in-bistro':
                    match = re.match(r'(\d{4}):([^:]+)', file.name)
                    if match:
                        year = match.group(1)
                        title = match.group(2).replace(':', ' ')
                
                clean_title = clean_filename(title)
                new_filename = f"{clean_title}.jpg"
                output_path = series_path / new_filename
                
                try:
                    optimize_image(file, output_path, max_width=2400, quality=95)
                    if file.name != new_filename:
                        file.unlink()
                    
                    series_info[series].append({
                        'filename': new_filename,
                        'title': title,
                        'year': year
                    })
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    
    return series_info

def update_gallery_js(series_info):
    root_dir = Path(__file__).parent.parent
    js_content = "const galleryData = {\n"
    
    for series, images in series_info.items():
        if not images:
            continue
            
        js_content += f"    '{series}': {{\n"
        js_content += f"        title: \"{series.replace('-', ' ').title()}\",\n"
        js_content += f"        period: \"{min(img['year'] for img in images)}-{max(img['year'] for img in images)}\",\n"
        js_content += "        images: [\n"
        
        for img in sorted(images, key=lambda x: x['filename']):
            js_content += "            {\n"
            js_content += f"                src: \"{img['filename']}\",\n"
            js_content += f"                title: \"{img['title']}\",\n"
            js_content += f"                year: \"{img['year']}\"\n"
            js_content += "            },\n"
        
        js_content += "        ]\n    },\n"
    
    js_content += "};\n\n"
    
    js_content += """
const galleryContainer = document.getElementById('gallery-container');
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const closeButton = document.querySelector('.close');

function createGalleryItem(image, series) {
    const galleryItem = document.createElement('div');
    galleryItem.className = 'gallery-item';

    const img = document.createElement('img');
    img.src = `images/gallery/${series}/${image.src}`;
    img.alt = image.title;
    img.loading = 'lazy';

    galleryItem.appendChild(img);
    img.addEventListener('click', () => openLightbox(img.src));

    return galleryItem;
}

function initGallery() {
    Object.entries(galleryData).forEach(([series, data]) => {
        data.images.forEach(image => {
            const item = createGalleryItem(image, series);
            galleryContainer.appendChild(item);
        });
    });
}

function openLightbox(imageSrc) {
    lightbox.classList.add('active');
    lightboxImg.src = imageSrc;
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    lightbox.classList.remove('active');
    lightboxImg.src = '';
    document.body.style.overflow = '';
}

closeButton.addEventListener('click', closeLightbox);
lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) {
        closeLightbox();
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lightbox.classList.contains('active')) {
        closeLightbox();
    }
});

document.addEventListener('DOMContentLoaded', initGallery);
"""
    
    with open(root_dir / 'js/gallery.js', 'w') as f:
        f.write(js_content)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'portfolio':
        print("Processing portfolio folder...")
        process_portfolio()
    elif len(sys.argv) > 1 and sys.argv[1] == 'lyahelia':
        print("Processing lyahelia folder...")
        process_lyahelia()
    else:
        folder_name = None
        if len(sys.argv) > 1:
            folder_name = sys.argv[1]
            
        series_info = process_gallery(folder_name)
        update_gallery_js(series_info) 