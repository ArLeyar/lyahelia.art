document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.main-nav a');
    const nav = document.querySelector('.main-nav');
    let lastScrollTop = 0;

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('href');
            
            // Only prevent default and do smooth scrolling for same-page links
            if (targetId.startsWith('#')) {
                e.preventDefault();
                const targetSection = document.querySelector(targetId);
                if (targetSection) {
                    const navHeight = nav.offsetHeight;
                    
                    window.scrollTo({
                        top: targetSection.offsetTop - navHeight,
                        behavior: 'smooth'
                    });
                }
            } 
            // Handle links with hash but not at the beginning (like "/#home")
            else if (targetId.includes('#') && !targetId.startsWith('/manifesto')) {
                // Only handle index.html page links that contain #
                // For other pages like /manifesto, let the browser navigate normally
                e.preventDefault();
                
                // Extract the hash part
                const hashPart = targetId.substring(targetId.indexOf('#'));
                const targetSection = document.querySelector(hashPart);
                
                if (targetSection) {
                    const navHeight = nav.offsetHeight;
                    
                    window.scrollTo({
                        top: targetSection.offsetTop - navHeight,
                        behavior: 'smooth'
                    });
                } else {
                    // If section not found, navigate normally
                    window.location.href = targetId;
                }
            }
            // For all other links (like "/manifesto"), do the default navigation
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