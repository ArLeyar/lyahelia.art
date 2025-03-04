# Website Utilities

This directory contains utility scripts for managing the Lya Helia Art website.

## Setup

1. Make sure you have Python 3.9+ installed
2. Install Poetry (package manager) if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Install dependencies:
   ```bash
   cd scripts
   poetry install
   ```

## Available Scripts

### Optimize Images

Processes and optimizes images in the gallery directories:

```bash
cd scripts
poetry run python optimize_images.py
```

This script:
- Processes images in `/images/gallery/{textures,elements,emotional-postcards,girl-in-bistro}`
- Converts HEIC files to JPEG
- Resizes large images (max width: 2000px)
- Optimizes JPEG quality (85%)
- Generates gallery.js with image metadata
- Supports image naming format: `YYYY:Title-Of-Image.jpg`

### Generate Favicons

Creates favicon files in various sizes from a source image:

```bash
cd scripts
poetry run python generate_favicons.py
```

This will generate:
- favicon.ico (16x16, 32x32, 48x48)
- favicon-16x16.png
- favicon-32x32.png
- apple-touch-icon.png (180x180)
- android-chrome-192x192.png
- android-chrome-512x512.png

### Generate Social Preview

Creates an optimized image for social media previews:

```bash
cd scripts
poetry run python generate_social_preview.py
```

This will generate a 1200x630 pixel image optimized for social media previews (Facebook, Twitter, Telegram, etc.). 