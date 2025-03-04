from PIL import Image
import os
import re
from pathlib import Path
import pillow_heif

def optimize_image(input_path, output_path, max_width=2000):
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
    
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, 'white')
        background.paste(img, mask=img.getchannel('A'))
        img = background
    
    width, height = img.size
    if width > max_width:
        ratio = max_width / width
        new_size = (max_width, int(height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    img.save(output_path, 'JPEG', quality=85, optimize=True)
    if hasattr(img, 'close'):
        img.close()

def clean_filename(filename):
    return re.sub(r'[^a-zA-Z0-9-]', '-', filename).lower()

def process_gallery():
    root_dir = Path(__file__).parent.parent
    gallery_path = root_dir / 'images/gallery'
    series_info = {
        'textures': [],
        'elements': [],
        'emotional-postcards': [],
        'girl-in-bistro': []
    }
    
    for series in series_info.keys():
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
                    optimize_image(file, output_path)
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
    series_info = process_gallery()
    update_gallery_js(series_info) 