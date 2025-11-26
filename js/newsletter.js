(function() {
    'use strict';
    
    // Determine base path based on current page location
    function getBasePath() {
        const path = window.location.pathname;
        if (path.includes('/pages/') || path.includes('/pages/portfolio/')) {
            return path.includes('/pages/portfolio/') ? '../../' : '../';
        }
        return '';
    }

    // Newsletter HTML template
    function getNewsletterHTML(basePath) {
        return `
        <section class="newsletter-section" id="newsletter" style="margin-top: 4rem;">
            <div class="newsletter-content">
                <div class="newsletter-portrait">
                    <img src="${basePath}images/portrait.jpg" alt="Lya Helia" class="portrait-image">
                </div>
                <div class="newsletter-text-content">
                    <h2 class="newsletter-title">Stay Connected</h2>
                    <p class="newsletter-description">Join my inner circle and be the first to know about new releases, exclusive offers, and behind-the-scenes insights into my creative process.</p>
                    
                    <div id="mlb2-33791224" class="ml-form-embedContainer ml-subscribe-form ml-subscribe-form-33791224">
                        <div class="ml-form-align-center">
                            <div class="ml-form-embedWrapper embedForm">
                                <div class="ml-form-embedBody ml-form-embedBodyDefault row-form">
                                    <form class="ml-block-form" action="https://assets.mailerlite.com/jsonp/1942698/forms/172017847721002674/subscribe" data-code="" method="post" target="hidden_iframe_mailerlite">
                                        <div class="ml-form-formContent">
                                            <div class="ml-form-fieldRow ml-last-item">
                                                <div class="ml-field-group ml-field-email ml-validate-email ml-validate-required">
                                                    <input aria-label="email" aria-required="true" type="email" class="form-control" data-inputmask="" name="fields[email]" placeholder="Email" autocomplete="email" style="width: 100%; padding: 1rem 1.25rem; font-size: 1rem; font-family: 'Quattrocento', serif; border: 2px solid #ddd; border-radius: 8px; margin-bottom: 1rem; background: white; color: #333; box-sizing: border-box;">
                                                </div>
                                            </div>
                                        </div>
                                        <input type="hidden" name="ml-submit" value="1">
                                        <div class="ml-form-embedSubmit">
                                            <button type="submit" class="primary" style="width: 100%; padding: 1rem 2rem; background: #333; color: white; border: none; border-radius: 8px; font-size: 1rem; font-family: 'Quattrocento', serif; font-weight: 600; cursor: pointer; text-transform: uppercase; letter-spacing: 1px;">Subscribe</button>
                                            <button disabled="disabled" style="display: none;" type="button" class="loading">
                                                <div class="ml-form-embedSubmitLoad"></div>
                                                <span class="sr-only">Loading...</span>
                                            </button>
                                        </div>
                                        <input type="hidden" name="anticsrf" value="true">
                                    </form>
                                </div>
                                <div class="ml-form-successBody row-success" style="display: none">
                                    <div class="ml-form-successContent">
                                        <h4>Thank you!</h4>
                                        <p>You have successfully joined our subscriber list.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <iframe name="hidden_iframe_mailerlite" id="hidden_iframe_mailerlite" style="display:none;"></iframe>
                    <p class="privacy-note">I respect your privacy. Unsubscribe at any time.</p>
                    
                    <div id="subscriptionPopup" class="subscription-popup" style="display: none;">
                        <div class="popup-content">
                            <span class="popup-close">&times;</span>
                            <h3>✓ Successfully Subscribed!</h3>
                            <p>Thank you for joining! Check your inbox for confirmation.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>`;
    }

    // Initialize newsletter
    function initNewsletter() {
        const basePath = getBasePath();
        const existingNewsletter = document.querySelector('.newsletter-section');
        
        // If newsletter already exists in HTML (like in blackfriday.html), just setup handlers
        if (existingNewsletter) {
            setupNewsletterHandlers();
            loadMailerLiteScripts();
            return;
        }
        
        // Otherwise, inject newsletter into page-content
        const pageContent = document.querySelector('.page-content');
        if (pageContent) {
            pageContent.insertAdjacentHTML('beforeend', getNewsletterHTML(basePath));
            setupNewsletterHandlers();
            loadMailerLiteScripts();
        }
    }

    // Setup event handlers
    function setupNewsletterHandlers() {
        // Handle form submission
        const newsletterForm = document.querySelector('.ml-subscribe-form-33791224 form');
        if (newsletterForm) {
            newsletterForm.addEventListener('submit', function(e) {
                setTimeout(function() {
                    const emailInput = newsletterForm.querySelector('input[type="email"]');
                    if (emailInput && emailInput.value) {
                        showPopup();
                        newsletterForm.reset();
                    }
                }, 1000);
            });
        }

        // Popup close handlers
        const popup = document.getElementById('subscriptionPopup');
        const popupClose = document.querySelector('.popup-close');

        if (popupClose) {
            popupClose.addEventListener('click', function() {
                popup.style.display = 'none';
            });
        }

        if (popup) {
            popup.addEventListener('click', function(e) {
                if (e.target === popup) {
                    popup.style.display = 'none';
                }
            });
        }

        // Listen for MailerLite success message
        window.addEventListener('message', function(event) {
            if (event.data === 'ml:success') {
                showPopup();
            }
        });
    }

    // Show success popup
    function showPopup() {
        const popup = document.getElementById('subscriptionPopup');
        if (popup) {
            popup.style.display = 'flex';
            setTimeout(() => {
                popup.style.display = 'none';
            }, 5000);
        }
    }

    // Load MailerLite scripts
    function loadMailerLiteScripts() {
        // Only load MailerLite Universal if not already loaded
        if (!window.ml) {
            (function(w,d,e,u,f,l,n){
                w[f]=w[f]||function(){(w[f].q=w[f].q||[]).push(arguments);};
                l=d.createElement(e);
                l.async=1;
                l.src=u;
                n=d.getElementsByTagName(e)[0];
                n.parentNode.insertBefore(l,n);
            })(window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');
            
            window.ml('account', '1942698');
        }

        // MailerLite success callback (always set this)
        window.ml_webform_success_33791224 = function() {
            var $ = window.ml_jQuery || window.jQuery;
            if ($) {
                $('.ml-subscribe-form-33791224 .row-success').hide();
                $('.ml-subscribe-form-33791224 .row-form').show();
            }
            showPopup();
            const form = document.querySelector('.ml-subscribe-form-33791224 form');
            if (form) form.reset();
        };

        // Load webforms script if not already loaded
        if (!document.querySelector('script[src*="webforms.min.js"]')) {
            const webformsScript = document.createElement('script');
            webformsScript.src = 'https://groot.mailerlite.com/js/w/webforms.min.js?v176e10baa5e7ed80d35ae235be3d5024';
            document.body.appendChild(webformsScript);
        }

        // Fetch form configuration
        fetch('https://assets.mailerlite.com/jsonp/1942698/forms/172017847721002674/takel');
    }

    // Hamburger menu functionality
    function initHamburgerMenu() {
        const hamburger = document.querySelector('.hamburger-menu');
        const nav = document.querySelector('.main-nav');
        
        if (hamburger && nav) {
            hamburger.addEventListener('click', function() {
                nav.classList.toggle('active');
                hamburger.classList.toggle('active');
            });
            
            const navLinks = document.querySelectorAll('.main-nav a');
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    nav.classList.remove('active');
                    hamburger.classList.remove('active');
                });
            });
        }
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initHamburgerMenu();
            initNewsletter();
        });
    } else {
        initHamburgerMenu();
        initNewsletter();
    }
})();

