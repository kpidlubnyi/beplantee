document.addEventListener('DOMContentLoaded', function() {
    initAddPlantPage();
    console.log('🌱 Add Plant page initialized');
});

let plantTypes = []; 
let selectedPlantId = null;

function initAddPlantPage() {
    initNameInput();
    initImageUpload();
    initDropdown();
    initFormValidation();
    loadPlantTypes();
}

function initNameInput() {
    const nameInput = document.getElementById('plantNameInput');
    const nameDisplay = document.getElementById('plantNameDisplay');
    const charCount = document.getElementById('charCount');
    
    if (!nameInput || !nameDisplay || !charCount) return;
    
    nameInput.addEventListener('input', function() {
        const value = this.value.trim();
        const length = this.value.length;
        
        charCount.textContent = length;
        
        if (value) {
            nameDisplay.textContent = value.toUpperCase();
        } else {
            nameDisplay.textContent = 'NEW PLANT';
        }
        
        if (length > 15) {
            charCount.style.color = 'var(--error-red)';
        } else if (length > 10) {
            charCount.style.color = 'var(--primary-green)';
        } else {
            charCount.style.color = 'var(--gray-text)';
        }
        
        validateForm();
    });
    
    nameInput.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    nameInput.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });
}

function initImageUpload() {
    const imageInput = document.getElementById('imageInput');
    const plantImage = document.getElementById('plantImage');
    const uploadArea = document.getElementById('imageUploadArea');
    const uploadButton = document.querySelector('.upload-button');
    
    if (!imageInput || !plantImage || !uploadArea) return;
    
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleImageUpload(file);
        }
    });
    
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            imageInput.files = e.dataTransfer.files;
            handleImageUpload(file);
        }
    });
    
    uploadButton.addEventListener('click', function(e) {
        e.stopPropagation();
        imageInput.click();
    });
}

function handleImageUpload(file) {
    const plantImage = document.getElementById('plantImage');
    const uploadArea = document.getElementById('imageUploadArea');
    
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
        showError('Image file size must be less than 5MB');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        plantImage.src = e.target.result;
        uploadArea.classList.add('has-image');
        
        showSuccess('Image uploaded successfully!');
    };
    
    reader.onerror = function() {
        showError('Failed to read image file');
    };
    
    reader.readAsDataURL(file);
}

function initDropdown() {
    const searchInput = document.getElementById('plantTypeSearch');
    const dropdownContainer = document.querySelector('.dropdown-container');
    const dropdownList = document.getElementById('dropdownList');
    const selectedPlantIdInput = document.getElementById('selectedPlantId');
    
    if (!searchInput || !dropdownContainer || !dropdownList) return;
    
    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        filterPlantTypes(query);
        openDropdown();
    });
    
    searchInput.addEventListener('focus', function() {
        openDropdown();
        if (plantTypes.length === 0) {
            loadPlantTypes();
        }
    });
    
    searchInput.addEventListener('blur', function() {
        setTimeout(() => closeDropdown(), 150);
    });
    
    searchInput.addEventListener('keydown', function(e) {
        const items = dropdownList.querySelectorAll('.dropdown-item:not(.hidden)');
        const currentSelected = dropdownList.querySelector('.dropdown-item.selected');
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                navigateDropdown('down', items, currentSelected);
                break;
            case 'ArrowUp':
                e.preventDefault();
                navigateDropdown('up', items, currentSelected);
                break;
            case 'Enter':
                e.preventDefault();
                if (currentSelected) {
                    selectPlantType(currentSelected);
                }
                break;
            case 'Escape':
                closeDropdown();
                break;
        }
    });
    
    document.addEventListener('click', function(e) {
        if (!dropdownContainer.contains(e.target)) {
            closeDropdown();
        }
    });
}

async function loadPlantTypes() {
    const dropdownList = document.getElementById('dropdownList');
    
    try {
        dropdownList.innerHTML = '<div class="dropdown-loading">Loading plant types...</div>';
        
        const response = await fetch('/api/plant-types');
        const data = await response.json();
        
        if (data.plant_types && data.plant_types.length > 0) {
            plantTypes = data.plant_types;
            renderDropdownItems(plantTypes);
        } else {
            dropdownList.innerHTML = '<div class="dropdown-no-results">No plant types available</div>';
        }
    } catch (error) {
        console.error('Error loading plant types:', error);
        dropdownList.innerHTML = '<div class="dropdown-no-results">Failed to load plant types</div>';
    }
}

function renderDropdownItems(items) {
    const dropdownList = document.getElementById('dropdownList');
    
    if (items.length === 0) {
        dropdownList.innerHTML = '<div class="dropdown-no-results">No matching plant types found</div>';
        return;
    }
    
    dropdownList.innerHTML = items.map(plant => `
        <div class="dropdown-item" data-id="${plant.id}" data-name="${plant.display_name || plant.common_name || plant.scientific_name}">
            ${plant.display_name || plant.common_name || plant.scientific_name}
        </div>
    `).join('');
    
    dropdownList.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', function() {
            selectPlantType(this);
        });
        
        item.addEventListener('mouseenter', function() {
            dropdownList.querySelectorAll('.dropdown-item').forEach(i => i.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
}

function filterPlantTypes(query) {
    if (!query) {
        renderDropdownItems(plantTypes);
        return;
    }
    
    const filtered = plantTypes.filter(plant => {
        const name = (plant.display_name || plant.common_name || plant.scientific_name || '').toLowerCase();
        return name.includes(query);
    });
    
    renderDropdownItems(filtered);
}

function navigateDropdown(direction, items, currentSelected) {
    if (items.length === 0) return;
    
    let nextIndex = 0;
    
    if (currentSelected) {
        const currentIndex = Array.from(items).indexOf(currentSelected);
        if (direction === 'down') {
            nextIndex = (currentIndex + 1) % items.length;
        } else {
            nextIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
        }
    }
    
    items.forEach(item => item.classList.remove('selected'));
    
    items[nextIndex].classList.add('selected');
    items[nextIndex].scrollIntoView({ block: 'nearest' });
}

function selectPlantType(item) {
    const searchInput = document.getElementById('plantTypeSearch');
    const selectedPlantIdInput = document.getElementById('selectedPlantId');
    
    const plantId = item.dataset.id;
    const plantName = item.dataset.name;
    
    searchInput.value = plantName;
    selectedPlantIdInput.value = plantId;
    selectedPlantId = plantId;
    
    closeDropdown();
    validateForm();
    
    console.log('Selected plant:', { id: plantId, name: plantName });
}

function openDropdown() {
    const dropdownContainer = document.querySelector('.dropdown-container');
    dropdownContainer.classList.add('open');
}

function closeDropdown() {
    const dropdownContainer = document.querySelector('.dropdown-container');
    dropdownContainer.classList.remove('open');
    
    const dropdownList = document.getElementById('dropdownList');
    dropdownList.querySelectorAll('.dropdown-item').forEach(item => {
        item.classList.remove('selected');
    });
}

function initFormValidation() {
    const form = document.getElementById('addPlantForm');
    const confirmBtn = document.getElementById('confirmBtn');
    
    if (!form || !confirmBtn) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm()) {
            submitForm();
        }
    });
}

function validateForm() {
    const nameInput = document.getElementById('plantNameInput');
    const confirmBtn = document.getElementById('confirmBtn');
    
    const hasName = nameInput.value.trim().length > 0;
    const hasPlantType = selectedPlantId !== null;
    
    const isValid = hasName && hasPlantType;
    
    confirmBtn.disabled = !isValid;
    confirmBtn.classList.toggle('valid', isValid);
    
    return isValid;
}

async function submitForm() {
    const form = document.getElementById('addPlantForm');
    const confirmBtn = document.getElementById('confirmBtn');
    
    try {
        confirmBtn.classList.add('loading');
        confirmBtn.disabled = true;
        
        form.submit();
        
    } catch (error) {
        console.error('Error submitting form:', error);
        showError('Failed to add plant. Please try again.');
        
        confirmBtn.classList.remove('loading');
        validateForm();
    }
}

function showError(message) {
    showNotification(message, 'error');
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showNotification(message, type = 'info') {
    if (window.BePlantee && window.BePlantee.showNotification) {
        window.BePlantee.showNotification(message, type);
    } else {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '12px 24px',
            borderRadius: '6px',
            color: 'white',
            fontWeight: '500',
            zIndex: '9999',
            transform: 'translateX(400px)',
            transition: 'transform 0.3s ease'
        });
        
        switch (type) {
            case 'success':
                notification.style.backgroundColor = '#27AE60';
                break;
            case 'error':
                notification.style.backgroundColor = '#E74C3C';
                break;
            default:
                notification.style.backgroundColor = '#3498DB';
        }
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

function resetForm() {
    const form = document.getElementById('addPlantForm');
    const nameDisplay = document.getElementById('plantNameDisplay');
    const plantImage = document.getElementById('plantImage');
    const uploadArea = document.getElementById('imageUploadArea');
    const charCount = document.getElementById('charCount');
    
    form.reset();
    nameDisplay.textContent = 'NEW PLANT';
    plantImage.src = '/uploads/default_plant.png';
    uploadArea.classList.remove('has-image');
    charCount.textContent = '0';
    selectedPlantId = null;
    
    validateForm();
    closeDropdown();
}

document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        if (plantTypes.length === 0) {
            loadPlantTypes();
        }
    }
});

window.AddPlant = {
    resetForm: resetForm,
    loadPlantTypes: loadPlantTypes,
    validateForm: validateForm
};