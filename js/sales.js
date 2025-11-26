// Sales page specific functionality

// Video toggle function
function toggleVideo() {
    const videoContent = document.getElementById('packagingVideo');
    const videoPreview = document.querySelector('.video-preview');
    const video = videoContent ? videoContent.querySelector('video') : null;
    
    if (!videoContent || !videoPreview || !video) return;
    
    if (videoContent.style.display === 'none') {
        videoContent.style.display = 'block';
        videoPreview.style.display = 'none';
        video.play().catch(e => {
            console.log('Autoplay prevented:', e);
        });
    } else {
        videoContent.style.display = 'none';
        videoPreview.style.display = 'block';
        video.pause();
        video.currentTime = 0;
    }
}

// Carousel functions
function changeSlide(carouselId, direction) {
    const carousel = document.getElementById(carouselId);
    if (!carousel) return;
    
    const slides = carousel.querySelectorAll('.carousel-slide');
    const dots = carousel.querySelectorAll('.dot');
    let currentIndex = 0;
    
    slides.forEach((slide, index) => {
        if (slide.classList.contains('active')) {
            currentIndex = index;
        }
    });
    
    slides[currentIndex].classList.remove('active');
    dots[currentIndex].classList.remove('active');
    
    let newIndex = currentIndex + direction;
    if (newIndex >= slides.length) newIndex = 0;
    if (newIndex < 0) newIndex = slides.length - 1;
    
    slides[newIndex].classList.add('active');
    dots[newIndex].classList.add('active');
}

function currentSlide(carouselId, slideNumber) {
    const carousel = document.getElementById(carouselId);
    if (!carousel) return;
    
    const slides = carousel.querySelectorAll('.carousel-slide');
    const dots = carousel.querySelectorAll('.dot');
    
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));
    
    slides[slideNumber - 1].classList.add('active');
    dots[slideNumber - 1].classList.add('active');
}

