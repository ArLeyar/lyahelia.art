const galleryData = {
    textures: {
        title: "Textures",
        period: "2021-2024",
        images: [
            {
                src: "a-feeling-of-freshly-falling-in-love.jpg",
                title: "A Feeling of Freshly Falling in Love",
                year: "2023"
            },
            {
                src: "a-boy-named-sun.jpg",
                title: "A Boy Named Sun",
                year: "2022"
            },
            {
                src: "healing.jpg",
                title: "Healing",
                year: "2022"
            },
            {
                src: "silver-gates.jpg",
                title: "Silver Gates",
                year: "2021"
            },
            {
                src: "by-the-sea.jpg",
                title: "By the Sea",
                year: "2024"
            },
            {
                src: "textures-6.jpg",
                title: "Textures 6",
                year: "2024"
            },
            {
                src: "textures-7.jpg",
                title: "Textures 7",
                year: "2024"
            },
        ]
    },
    elements: {
        title: "Elements",
        period: "2024",
        images: [
            {
                src: "elements-1.jpg",
                title: "Elements 1",
                year: "2024"
            },
            {
                src: "elements-2.jpg",
                title: "Elements 2",
                year: "2024"
            },
            {
                src: "elements-3.jpg",
                title: "Elements 3",
                year: "2024"
            },
            {
                src: "elements-4.jpg",
                title: "Elements 4",
                year: "2024"
            },
        ]
    },
    'emotional-postcards': {
        title: "Emotional Postcards",
        period: "2024",
        images: [
            {
                src: "emotional-postcards-1.jpg",
                title: "Emotional Postcards 1",
                year: "2024"
            },
            {
                src: "emotional-postcards-2.jpg",
                title: "Emotional Postcards 2",
                year: "2024"
            },
            {
                src: "emotional-postcards-3.jpg",
                title: "Emotional Postcards 3",
                year: "2024"
            },
            {
                src: "emotional-postcards-4.jpg",
                title: "Emotional Postcards 4",
                year: "2024"
            },
            {
                src: "emotional-postcards-5.jpg",
                title: "Emotional Postcards 5",
                year: "2024"
            },
            {
                src: "emotional-postcards-6.jpg",
                title: "Emotional Postcards 6",
                year: "2024"
            },
        ]
    },
    'girl-in-bistro': {
        title: "Girl in Bistro",
        period: "2024",
        images: [
            {
                src: "girl-in-bistro-1.jpg",
                title: "Girl in Bistro 1",
                year: "2024"
            },
            {
                src: "girl-in-bistro-2.jpg",
                title: "Girl in Bistro 2",
                year: "2024"
            },
            {
                src: "girl-in-bistro-3.jpg",
                title: "Girl in Bistro 3",
                year: "2024"
            },
            {
                src: "girl-in-bistro-4.jpg",
                title: "Girl in Bistro 4",
                year: "2024"
            },
            {
                src: "girl-in-bistro-5.jpg",
                title: "Girl in Bistro 5",
                year: "2024"
            },
            {
                src: "girl-in-bistro-6.jpg",
                title: "Girl in Bistro 6",
                year: "2024"
            },
            {
                src: "girl-in-bistro-7.jpg",
                title: "Girl in Bistro 7",
                year: "2024"
            },
        ]
    }
};

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
