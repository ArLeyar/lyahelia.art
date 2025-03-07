document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.main-nav a');
    const nav = document.querySelector('.main-nav');
    let lastScrollTop = 0;

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Only handle same-page links (starting with #)
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetSection = document.querySelector(href);
                if (targetSection) {
                    const navHeight = nav.offsetHeight;
                    window.scrollTo({
                        top: targetSection.offsetTop - navHeight,
                        behavior: 'smooth'
                    });
                }
            }
            // Special case for links like "/#section" - only from index page to index page
            else if (href.startsWith('/#') && window.location.pathname === '/' || window.location.pathname === '/index.html') {
                e.preventDefault();
                const hashPart = href.substring(href.indexOf('#'));
                const targetSection = document.querySelector(hashPart);
                if (targetSection) {
                    const navHeight = nav.offsetHeight;
                    window.scrollTo({
                        top: targetSection.offsetTop - navHeight,
                        behavior: 'smooth'
                    });
                } else {
                    // If target not found, follow the link normally
                    window.location.href = href;
                }
            }
            // All other links (like "/manifesto") - let browser handle normally
            // No preventDefault() means normal navigation occurs
        });
    });

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop) {
            nav.style.transform = 'translateY(-100%)';
        } else {
            nav.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
}); 