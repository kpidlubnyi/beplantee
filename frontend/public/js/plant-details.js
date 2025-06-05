document.addEventListener('DOMContentLoaded', function() {
    initPlantDetailsPage();
    console.log('🌱 Plant Details page initialized');
});

function initPlantDetailsPage() {
    initScrollAnimations();
    initCopyLinkFunctionality();
    initAddToCollectionButton();
    enhanceAccessibility();
    
    const detailItems = document.querySelectorAll('.detail-item');
    detailItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.05}s`;
    });
}

function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                if (entry.target.classList.contains('detail-item')) {
                    const siblings = Array.from(entry.target.parentNode.children);
                    const index = siblings.indexOf(entry.target);
                    entry.target.style.animationDelay = `${index * 0.05}s`;
                }
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.detail-item, .description-section, .care-section').forEach(el => {
        observer.observe(el);
    });
}

function initCopyLinkFunctionality() {
    const externalLink = document.querySelector('.external-link-url');
    
    if (externalLink) {
        externalLink.style.cursor = 'pointer';
        externalLink.title = 'Click to copy link';
        
        externalLink.addEventListener('click', function() {
            const linkText = this.textContent;
            
            if (navigator.clipboard) {
                navigator.clipboard.writeText(linkText).then(() => {
                    showCopyFeedback(this);
                }).catch(err => {
                    console.error('Failed to copy link:', err);
                });
            } else {
                const textArea = document.createElement('textarea');
                textArea.value = linkText;
                document.body.appendChild(textArea);
                textArea.select();
                
                try {
                    document.execCommand('copy');
                    showCopyFeedback(this);
                } catch (err) {
                    console.error('Failed to copy link:', err);
                }
                
                document.body.removeChild(textArea);
            }
        });
    }
}

function showCopyFeedback(element) {
    const originalText = element.textContent;
    element.textContent = 'Link copied to clipboard!';
    element.style.color = 'var(--success-green)';
    element.style.fontWeight = 'bold';
    
    setTimeout(() => {
        element.textContent = originalText;
        element.style.color = '';
        element.style.fontWeight = '';
    }, 2000);
}

function initAddToCollectionButton() {
    const addButton = document.querySelector('.add-to-collection-btn');
    
    if (addButton) {
        addButton.addEventListener('click', function(e) {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            const plantName = this.textContent.trim();
            console.log('Adding plant to collection:', plantName);
        });
        
        addButton.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    }
}

function enhanceAccessibility() {
    const plantName = document.querySelector('.plant-name');
    if (plantName) {
        document.title = `${plantName.textContent} - Plant Details - BePlantee`;
    }
    
    const detailItems = document.querySelectorAll('.detail-item');
    detailItems.forEach(item => {
        const label = item.querySelector('.detail-label');
        const value = item.querySelector('.detail-value');
        
        if (label && value) {
            const labelId = `label-${Math.random().toString(36).substr(2, 9)}`;
            label.id = labelId;
            value.setAttribute('aria-labelledby', labelId);
        }
    });
    
    const plantIllustration = document.querySelector('.plant-illustration');
    if (plantIllustration) {
        plantIllustration.setAttribute('role', 'img');
        plantIllustration.setAttribute('aria-label', 'Plant illustration');
    }
}

function highlightToxicityInfo() {
    const detailItems = document.querySelectorAll('.detail-item');
    
    detailItems.forEach(item => {
        const label = item.querySelector('.detail-label');
        const value = item.querySelector('.detail-value');
        
        if (label && value) {
            const labelText = label.textContent.toLowerCase();
            const valueText = value.textContent.toLowerCase();
            
            if (labelText.includes('poisonous') && valueText.includes('1')) {
                value.classList.add('warning');
                value.textContent = 'Yes - Toxic ⚠️';
            } else if (labelText.includes('poisonous') && valueText.includes('0')) {
                value.classList.add('safe');
                value.textContent = 'No - Safe ✅';
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        highlightToxicityInfo();
    }, 100);
});

document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        console.log('Plant details page became visible');
    }
});

function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initPrintFunctionality() {
    window.addEventListener('beforeprint', function() {
        document.body.classList.add('printing');
    });
    
    window.addEventListener('afterprint', function() {
        document.body.classList.remove('printing');
    });
}

initSmoothScrolling();
initPrintFunctionality();

window.PlantDetails = {
    copyLink: () => {
        const link = document.querySelector('.external-link-url');
        if (link) link.click();
    },
    highlightToxicity: highlightToxicityInfo
};