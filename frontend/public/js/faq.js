document.addEventListener('DOMContentLoaded', function() {
    initFAQ();
    console.log('🌱 FAQ page initialized');
});

function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        
        if (question && answer) {
            question.addEventListener('click', function() {
                toggleFAQItem(item);
            });
            
            question.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleFAQItem(item);
                }
            });
        }
    });
    
    faqItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
    });
}

function toggleFAQItem(item) {
    const isActive = item.classList.contains('active');
    const answer = item.querySelector('.faq-answer');
    
    if (isActive) {
        item.classList.remove('active');
        answer.style.maxHeight = '0px';
    } else {
        const category = item.closest('.faq-category');
        const otherItems = category.querySelectorAll('.faq-item.active');
        otherItems.forEach(otherItem => {
            if (otherItem !== item) {
                otherItem.classList.remove('active');
                const otherAnswer = otherItem.querySelector('.faq-answer');
                otherAnswer.style.maxHeight = '0px';
            }
        });
        
        item.classList.add('active');
        
        const answerContent = answer.querySelector('.answer-content');
        const contentHeight = answerContent.scrollHeight;
        answer.style.maxHeight = `${contentHeight + 50}px`; 
        
        setTimeout(() => {
            const rect = item.getBoundingClientRect();
            const isVisible = rect.top >= 0 && rect.bottom <= window.innerHeight;
            
            if (!isVisible) {
                item.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }
        }, 300);
    }
    
    const question = item.querySelector('.faq-question');
    const expanded = item.classList.contains('active');
    question.setAttribute('aria-expanded', expanded.toString());
}

function expandAllFAQ() {
    const faqItems = document.querySelectorAll('.faq-item:not(.active)');
    faqItems.forEach(item => {
        toggleFAQItem(item);
    });
}

function collapseAllFAQ() {
    const faqItems = document.querySelectorAll('.faq-item.active');
    faqItems.forEach(item => {
        toggleFAQItem(item);
    });
}

function searchFAQ(query) {
    const faqItems = document.querySelectorAll('.faq-item');
    const searchTerm = query.toLowerCase();
    
    if (!searchTerm) {
        faqItems.forEach(item => {
            item.style.display = 'block';
        });
        return;
    }
    
    faqItems.forEach(item => {
        const question = item.querySelector('.question-text').textContent.toLowerCase();
        const answer = item.querySelector('.answer-content p').textContent.toLowerCase();
        
        if (question.includes(searchTerm) || answer.includes(searchTerm)) {
            item.style.display = 'block';
            highlightSearchTerm(item, searchTerm);
        } else {
            item.style.display = 'none';
        }
    });
}

function highlightSearchTerm(item, searchTerm) {
    const questionText = item.querySelector('.question-text');
    const answerText = item.querySelector('.answer-content p');
    
    [questionText, answerText].forEach(element => {
        const originalText = element.textContent;
        const regex = new RegExp(`(${searchTerm})`, 'gi');
        const highlightedText = originalText.replace(regex, '<mark>$1</mark>');
        
        if (highlightedText !== originalText) {
            element.innerHTML = highlightedText;
        }
    });
}

document.addEventListener('keydown', function(e) {
    if (e.target.classList.contains('faq-question')) {
        const currentItem = e.target.closest('.faq-item');
        const allItems = Array.from(document.querySelectorAll('.faq-item'));
        const currentIndex = allItems.indexOf(currentItem);
        
        let targetIndex = currentIndex;
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                targetIndex = Math.min(currentIndex + 1, allItems.length - 1);
                break;
            case 'ArrowUp':
                e.preventDefault();
                targetIndex = Math.max(currentIndex - 1, 0);
                break;
            case 'Home':
                e.preventDefault();
                targetIndex = 0;
                break;
            case 'End':
                e.preventDefault();
                targetIndex = allItems.length - 1;
                break;
        }
        
        if (targetIndex !== currentIndex) {
            const targetQuestion = allItems[targetIndex].querySelector('.faq-question');
            targetQuestion.focus();
        }
    }
});

window.FAQ = {
    expandAll: expandAllFAQ,
    collapseAll: collapseAllFAQ,
    search: searchFAQ
};