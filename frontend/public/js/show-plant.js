document.addEventListener('DOMContentLoaded', function() {
    initPlantShowPage();
    console.log('🌱 Plant Show page initialized');
});

function initPlantShowPage() {
    initCareButtons();
    initDeleteModal();
    initImageLoadError();
    enhanceAccessibility();
}

function initCareButtons() {
    const waterBtn = document.querySelector('.water-btn');
    const sunfillBtn = document.querySelector('.sunfill-btn');
    
    if (waterBtn) {
        waterBtn.addEventListener('click', function() {
            this.classList.add('loading');
            this.disabled = true;
        });
    }
    
    if (sunfillBtn) {
        sunfillBtn.addEventListener('click', function() {
            this.classList.add('loading');
            this.disabled = true;
        });
    }
}

function initDeleteModal() {
    const deleteBtn = document.querySelector('.delete-plant-btn');
    const modal = document.getElementById('deleteModal');
    const confirmBtn = document.querySelector('.confirm-delete-btn');
    const cancelBtn = document.querySelector('.cancel-btn');
    
    if (deleteBtn && modal) {
        deleteBtn.addEventListener('click', showDeleteModal);
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', hideDeleteModal);
    }
    
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                hideDeleteModal();
            }
        });
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
            hideDeleteModal();
        }
    });
}

function showDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        setTimeout(() => {
            const cancelBtn = modal.querySelector('.cancel-btn');
            if (cancelBtn) cancelBtn.focus();
        }, 100);
    }
}

function hideDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        
        const deleteBtn = document.querySelector('.delete-plant-btn');
        if (deleteBtn) deleteBtn.focus();
    }
}

async function waterPlant(plantId) {
    try {
        const response = await fetch(`/plants/${plantId}/water`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            showNotification('Plant watered successfully! 💧', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            throw new Error('Failed to water plant');
        }
    } catch (error) {
        console.error('Error watering plant:', error);
        showNotification('Failed to water plant', 'error');
        
        const waterBtn = document.querySelector('.water-btn');
        if (waterBtn) {
            waterBtn.classList.remove('loading');
            waterBtn.disabled = false;
        }
    }
}

async function sunfillPlant(plantId) {
    try {
        const response = await fetch(`/plants/${plantId}/sunfill`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            showNotification('Sunlight recorded successfully! ☀️', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            throw new Error('Failed to record sunlight');
        }
    } catch (error) {
        console.error('Error recording sunlight:', error);
        showNotification('Failed to record sunlight', 'error');
        
        const sunfillBtn = document.querySelector('.sunfill-btn');
        if (sunfillBtn) {
            sunfillBtn.classList.remove('loading');
            sunfillBtn.disabled = false;
        }
    }
}

async function confirmDelete(plantId) {
    const confirmBtn = document.querySelector('.confirm-delete-btn');
    
    if (confirmBtn) {
        confirmBtn.classList.add('loading');
        confirmBtn.disabled = true;
    }
    
    try {
        const response = await fetch(`/plants/${plantId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            showNotification('Plant deleted successfully', 'success');
            setTimeout(() => {
                window.location.href = '/plants';
            }, 1000);
        } else {
            throw new Error('Failed to delete plant');
        }
    } catch (error) {
        console.error('Error deleting plant:', error);
        showNotification('Failed to delete plant', 'error');
        
        if (confirmBtn) {
            confirmBtn.classList.remove('loading');
            confirmBtn.disabled = false;
        }
        hideDeleteModal();
    }
}

function initImageLoadError() {
    const plantImage = document.querySelector('.plant-photo-large');
    if (plantImage) {
        plantImage.addEventListener('error', function() {
            console.log('Plant image failed to load, using default');
            this.src = '/uploads/default_plant.png';
        });
    }
}

function enhanceAccessibility() {
    const infoBtn = document.querySelector('.info-btn');
    const editBtn = document.querySelector('.edit-btn');
    const deleteBtn = document.querySelector('.delete-plant-btn');
    
    if (infoBtn) {
        infoBtn.setAttribute('aria-label', 'View plant information');
    }
    
    if (editBtn) {
        editBtn.setAttribute('aria-label', 'Edit plant details');
    }
    
    if (deleteBtn) {
        deleteBtn.setAttribute('aria-label', 'Delete plant');
    }
    
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');
        modal.setAttribute('aria-labelledby', 'modal-title');
    }
}

function showNotification(message, type = 'info') {
    if (window.BePlantee && window.BePlantee.showNotification) {
        window.BePlantee.showNotification(message, type);
    } else {
        console.log(`${type}: ${message}`);
        alert(message);
    }
}

document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        console.log('Plant show page became visible');
    }
});

window.waterPlant = waterPlant;
window.sunfillPlant = sunfillPlant;
window.confirmDelete = confirmDelete;
window.showDeleteModal = showDeleteModal;
window.hideDeleteModal = hideDeleteModal;