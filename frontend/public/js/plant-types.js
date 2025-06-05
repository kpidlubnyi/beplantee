document.addEventListener('DOMContentLoaded', function() {
    initPlantTypesPage();
    console.log('🌱 Plant Types page initialized');
});

function initPlantTypesPage() {
    initSearch();
    initPlantTypeItems();
    
    const plantItems = document.querySelectorAll('.plant-type-item');
    plantItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.05}s`;
    });
}

function initSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    
    if (!searchForm || !searchInput) return;
    
    const urlParams = new URLSearchParams(window.location.search);
    if (!urlParams.get('search')) {
        searchInput.focus();
    }
    
    searchForm.addEventListener('submit', function(e) {
        const query = searchInput.value.trim();
        
        if (!query) {
            e.preventDefault();
            window.location.href = '/plant-types';
            return;
        }
        
        if (searchBtn) {
            searchBtn.textContent = 'Searching...';
            searchBtn.disabled = true;
        }
    });
    
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length >= 2) {
            searchTimeout = setTimeout(() => {
                console.log('Searching for:', query);
            }, 300);
        }
    });
    
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            searchForm.dispatchEvent(new Event('submit'));
        }
    });
    
    window.clearSearch = function() {
        window.location.href = '/plant-types';
    };
}

function initPlantTypeItems() {
    const plantItems = document.querySelectorAll('.plant-type-item');
    
    plantItems.forEach(item => {
        item.addEventListener('click', function(e) {
            const plantName = this.textContent.trim();
            console.log('Clicked on plant type:', plantName);
            
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
        
        item.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        item.addEventListener('mouseenter', function() {
        });
    });
    
    initKeyboardNavigation();
}

function initKeyboardNavigation() {
    const plantItems = Array.from(document.querySelectorAll('.plant-type-item'));
    
    plantItems.forEach((item, index) => {
        item.addEventListener('keydown', function(e) {
            let targetIndex = index;
            
            switch(e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    targetIndex = Math.min(index + 2, plantItems.length - 1);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    targetIndex = Math.max(index - 2, 0);
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    targetIndex = Math.min(index + 1, plantItems.length - 1);
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    targetIndex = Math.max(index - 1, 0);
                    break;
                case 'Home':
                    e.preventDefault();
                    targetIndex = 0;
                    break;
                case 'End':
                    e.preventDefault();
                    targetIndex = plantItems.length - 1;
                    break;
            }
            
            if (targetIndex !== index) {
                plantItems[targetIndex].focus();
            }
        });
    });
}

function debounceSearch(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

async function performLiveSearch(query) {
    if (query.length < 2) return;
    
    try {
        const response = await fetch(`/api/plant-types?search=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        updateSearchResults(data.plant_types || []);
    } catch (error) {
        console.error('Search error:', error);
    }
}

function updateSearchResults(plantTypes) {
    const grid = document.querySelector('.plant-types-grid');
    if (!grid) return;
    
    if (plantTypes.length === 0) {
        grid.innerHTML = '<div class="empty-state"><h3>No results found</h3><p>Try different search terms</p></div>';
        return;
    }
    
    grid.innerHTML = plantTypes.map(plant => `
        <a href="/plant-types/${plant.id}" class="plant-type-item">
            ${plant.display_name || plant.common_name || plant.scientific_name}
        </a>
    `).join('');
    
    initPlantTypeItems();
}

function showLoading() {
    const content = document.querySelector('.plant-types-content');
    if (content) {
        content.innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p class="loading-text">Loading plant types...</p>
            </div>
        `;
    }
}

document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        console.log('Plant types page became visible');
    }
});

window.PlantTypes = {
    clearSearch: () => window.location.href = '/plant-types',
    performSearch: performLiveSearch,
    showLoading: showLoading
};