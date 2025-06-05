document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm') || document.getElementById('loginForm');
    if (!form) return;

    const submitBtn = form.querySelector('.auth-submit-btn');
    const inputs = form.querySelectorAll('.form-input');

    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            validateInput(this);
        });

        input.addEventListener('input', function() {
            clearInputError(this);
        });
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }

        setLoading(true);
        
        try {
            this.submit();
        } catch (error) {
            console.error('Form submission error:', error);
            setLoading(false);
            showError('An error occurred. Please try again.');
        }
    });

    function validateForm() {
        let isValid = true;
        const formData = new FormData(form);
        
        clearAllErrors();

        const username = formData.get('username');
        if (!username || username.trim().length < 3) {
            showInputError('username', 'Username must be at least 3 characters long');
            isValid = false;
        }

        const emailInput = form.querySelector('input[name="email"]');
        if (emailInput) {
            const email = formData.get('email');
            if (!email || !isValidEmail(email)) {
                showInputError('email', 'Please enter a valid email address');
                isValid = false;
            }
        }

        const password = formData.get('password');
        if (!password || password.length < 8) {
            showInputError('password', 'Password must be at least 8 characters long');
            isValid = false;
        }

        if (emailInput && password) {
            const passwordErrors = validatePassword(password);
            if (passwordErrors.length > 0) {
                showInputError('password', passwordErrors[0]);
                isValid = false;
            }
        }

        return isValid;
    }

    function validateInput(input) {
        const value = input.value.trim();
        const name = input.name;

        clearInputError(input);

        switch (name) {
            case 'username':
                if (value.length > 0 && value.length < 3) {
                    showInputError('username', 'Username must be at least 3 characters long');
                }
                break;
            case 'email':
                if (value.length > 0 && !isValidEmail(value)) {
                    showInputError('email', 'Please enter a valid email address');
                }
                break;
            case 'password':
                if (value.length > 0 && value.length < 8) {
                    showInputError('password', 'Password must be at least 8 characters long');
                }
                break;
        }
    }

    function validatePassword(password) {
        const errors = [];
        
        if (password.length < 8) {
            errors.push('Password must be at least 8 characters long');
        }
        
        if (!/[A-Z]/.test(password)) {
            errors.push('Password must contain at least one uppercase letter');
        }
        
        if (!/[a-z]/.test(password)) {
            errors.push('Password must contain at least one lowercase letter');
        }
        
        if (!/[0-9]/.test(password)) {
            errors.push('Password must contain at least one digit');
        }
        
        if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
            errors.push('Password must contain at least one special character');
        }

        return errors;
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function showInputError(inputName, message) {
        const input = form.querySelector(`input[name="${inputName}"]`);
        if (!input) return;

        input.classList.add('error');
        
        const existingError = input.parentElement.querySelector('.input-error');
        if (existingError) {
            existingError.remove();
        }

        const errorElement = document.createElement('div');
        errorElement.className = 'input-error';
        errorElement.textContent = message;
        input.parentElement.appendChild(errorElement);
    }

    function clearInputError(input) {
        input.classList.remove('error');
        const errorElement = input.parentElement.querySelector('.input-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    function clearAllErrors() {
        inputs.forEach(input => {
            clearInputError(input);
        });
    }

    function showError(message) {
        let errorContainer = document.querySelector('.error-messages');
        if (!errorContainer) {
            errorContainer = document.createElement('div');
            errorContainer.className = 'error-messages';
            form.insertBefore(errorContainer, form.firstChild);
        }

        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.textContent = message;
        
        errorContainer.innerHTML = '';
        errorContainer.appendChild(errorElement);
    }

    function setLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            submitBtn.classList.add('loading');
        } else {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
        }
    }

    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(error => {
        setTimeout(() => {
            error.style.opacity = '0';
            setTimeout(() => {
                if (error.parentElement) {
                    error.remove();
                }
            }, 300);
        }, 5000);
    });
});

const style = document.createElement('style');
style.textContent = `
    .form-input.error {
        background: #ffebee !important;
        border: 2px solid var(--error-red) !important;
    }
    
    .input-error {
        color: var(--error-red);
        font-size: 12px;
        margin-top: 5px;
        margin-left: 20px;
        font-weight: 500;
    }
    
    .form-group.focused .form-input {
        transform: scale(1.02);
    }
`;
document.head.appendChild(style);