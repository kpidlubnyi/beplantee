
document.addEventListener('DOMContentLoaded', function() {
    initPlantsPage();
    console.log('🌱 My Plants page initialized');
});

function initPlantsPage() {
    initCareIndicators();
    initPlantCards();
    initScrollAnimations();
    initAddPlantButton();
    enhanceAccessibility();
}

function initCareIndicators() {
    const indicators = document.querySelectorAll('.care-indicator');
    
    indicators.forEach(indicator => {
        const level = parseInt(indicator.dataset.level) || 1;
        
        updateIndicatorColor(indicator, level);
        
        indicator.addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
            showCareInfo(this);
        });
        
        indicator.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.15)';
        });
        
        indicator.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

function updateIndicatorColor(indicator, level) {
    for (let i = 1; i <= 5; i++) {
        indicator.classList.remove(`level-${i}`);
    }
    
    indicator.classList.add(`level-${level}`);
    
    const colors = {
        1: '#FEFEF6',
        2: '#FFC1C1', 
        3: '#FFA3A3', 
        4: '#FF8484', 
        5: '#FF6666'  
    };
    
    const color = colors[level] || colors[1];
    indicator.style.setProperty('--indicator-color', color);
    
    const icon = indicator.querySelector('.care-icon');
    if (icon) {
        icon.style.color = color;
    }
}

function showCareInfo(indicator) {
    const level = parseInt(indicator.dataset.level) || 1;
    const isWatering = indicator.classList.contains('watering-indicator');
    const type = isWatering ? 'watering' : 'sunlight';
    
    const messages = {
        watering: {
            1: 'Recently watered 💧',
            2: 'Watering soon 💧',
            3: 'Needs watering 💧💧',
            4: 'Urgently needs water 💧💧💧',
            5: 'Critical - water now! 🚨💧'
        },
        sunlight: {
            1: 'Good sunlight ☀️',
            2: 'Could use more sun ☀️',
            3: 'Needs sunlight ☀️☀️',
            4: 'Urgently needs sun ☀️☀️☀️',
            5: 'Critical - needs sun! 🚨☀️'
        }
    };
    
    const message = messages[type][level] || 'Unknown status';
    
    showTemporaryTooltip(indicator, message);
}

function showTemporaryTooltip(element, message) {
    const existingTooltip = document.querySelector('.temp-tooltip');
    if (existingTooltip) {
        existingTooltip.remove();
    }
    
    const tooltip = document.createElement('div');
    tooltip.className = 'temp-tooltip';
    tooltip.textContent = message;
    
    Object.assign(tooltip.style, {
        position: 'absolute',
        background: 'rgba(0, 0, 0, 0.9)',
        color: 'white',
        padding: '8px 12px',
        borderRadius: '6px',
        fontSize: '12px',
        fontWeight: '500',
        zIndex: '10000',
        pointerEvents: 'none',
        whiteSpace: 'nowrap',
        transform: 'translateX(-50%)',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)'
    });
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + rect.width / 2 + 'px';
    tooltip.style.top = rect.bottom + 10 + 'px';
    
    setTimeout(() => {
        if (tooltip.parentNode) {
            tooltip.remove();
        }
    }, 2000);
}

function initPlantCards() {
    const plantCards = document.querySelectorAll('.plant-card');
    
    plantCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.closest('.care-indicator')) {
                return;
            }
            
            const plantId = this.dataset.plantId;
            const plantName = this.querySelector('.plant-name')?.textContent?.trim();
            
            console.log('Viewing plant:', { id: plantId, name: plantName });
            
            this.style.opacity = '0.7';
        });
        
        const link = card.querySelector('.plant-card-link');
        if (link) {
            link.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.click();
                }
            });
        }

        const plantImage = card.querySelector('.plant-photo');
            if (plantImage) {
                plantImage.addEventListener('error', function() {
                    const fallbackSrc = this.dataset.fallback;
                    if (fallbackSrc && this.src !== fallbackSrc) {
                        console.log('Image failed to load, using fallback:', fallbackSrc);
                        this.src = fallbackSrc;
                    }
                });
            }
        
        const index = Array.from(plantCards).indexOf(card);
        card.style.animationDelay = `${index * 0.1}s`;
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
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.plant-card').forEach(card => {
        observer.observe(card);
    });
}

function initAddPlantButton() {
    const addButton = document.querySelector('.add-plant-btn');
    
    if (addButton) {
        addButton.addEventListener('click', function(e) {
            this.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
        
        addButton.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        setInterval(() => {
            if (!addButton.matches(':hover')) {
                addButton.style.transform = 'translateY(-3px)';
                setTimeout(() => {
                    addButton.style.transform = 'translateY(0)';
                }, 1000);
            }
        }, 3000);
    }
}

function enhanceAccessibility() {
    const wateringIndicators = document.querySelectorAll('.watering-indicator');
    const sunlightIndicators = document.querySelectorAll('.sunlight-indicator');
    
    wateringIndicators.forEach(indicator => {
        const level = indicator.dataset.level || 1;
        indicator.setAttribute('aria-label', `Watering level ${level} out of 5`);
        indicator.setAttribute('role', 'img');
    });
    
    sunlightIndicators.forEach(indicator => {
        const level = indicator.dataset.level || 1;
        indicator.setAttribute('aria-label', `Sunlight level ${level} out of 5`);
        indicator.setAttribute('role', 'img');
    });
    
    const plantCards = document.querySelectorAll('.plant-card');
    plantCards.forEach(card => {
        const plantName = card.querySelector('.plant-name')?.textContent?.trim();
        if (plantName) {
            card.setAttribute('aria-label', `View details for ${plantName}`);
        }
    });
}

function refreshPlantData() {
    fetch('/plants')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newGrid = doc.querySelector('.plants-grid');
            const currentGrid = document.querySelector('.plants-grid');
            
            if (newGrid && currentGrid) {
                currentGrid.innerHTML = newGrid.innerHTML;
                initCareIndicators();
                initPlantCards();
            }
        })
        .catch(error => {
            console.error('Error refreshing plant data:', error);
            showNotification('Failed to refresh plant data', 'error');
        });
}

function showLoadingState() {
    const grid = document.querySelector('.plants-grid');
    if (!grid) return;
    
    const loadingHTML = Array(6).fill().map(() => `
        <div class="loading-card">
            <div class="loading-image"></div>
            <div class="loading-name"></div>
        </div>
    `).join('');
    
    grid.innerHTML = loadingHTML;
}

function showNotification(message, type = 'info') {
    if (window.BePlantee && window.BePlantee.showNotification) {
        window.BePlantee.showNotification(message, type);
    } else {
        console.log(`${type}: ${message}`);
    }
}

async function updateCareLevel(plantId, careType) {
    try {
        const response = await fetch(`/plants/${plantId}/${careType}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            showNotification(`${careType} recorded successfully!`, 'success');
            refreshPlantCard(plantId);
        } else {
            throw new Error('Failed to update care level');
        }
    } catch (error) {
        console.error('Error updating care level:', error);
        showNotification(`Failed to record ${careType}`, 'error');
    }
}

async function refreshPlantCard(plantId) {
    try {
        const response = await fetch(`/plants/${plantId}`);
        if (response.ok) {
            setTimeout(() => {
                refreshPlantData();
            }, 1000);
        }
    } catch (error) {
        console.error('Error refreshing plant card:', error);
    }
}

document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        const lastRefresh = localStorage.getItem('lastPlantsRefresh');
        const now = Date.now();
        
        if (!lastRefresh || now - parseInt(lastRefresh) > 5 * 60 * 1000) {
            refreshPlantData();
            localStorage.setItem('lastPlantsRefresh', now.toString());
        }
    }
});

setInterval(() => {
    if (document.visibilityState === 'visible') {
        refreshPlantData();
        localStorage.setItem('lastPlantsRefresh', Date.now().toString());
    }
}, 10 * 60 * 1000);

window.addEventListener('online', function() {
    showNotification('Connection restored', 'success');
    refreshPlantData();
});

window.addEventListener('offline', function() {
    showNotification('Connection lost - some features may not work', 'warning');
});

window.Plants = {
    refreshData: refreshPlantData,
    updateCareLevel: updateCareLevel,
    showLoading: showLoadingState
};