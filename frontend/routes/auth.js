const express = require('express');
const axios = require('axios');
const router = express.Router();

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

router.get('/register', (req, res) => {
  if (req.session.user) {
    return res.redirect('/dashboard');
  }
  res.render('auth/register', {
    title: 'Sign Up - BePlantee',
    errors: null,
    formData: {}
  });
});

router.post('/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    
    const errors = [];
    if (!username || username.length < 3) {
      errors.push('Username must be at least 3 characters long');
    }
    if (!email || !email.includes('@')) {
      errors.push('Please enter a valid email address');
    }
    if (!password || password.length < 8) {
      errors.push('Password must be at least 8 characters long');
    }
    
    if (errors.length > 0) {
      return res.render('auth/register', {
        title: 'Sign Up - BePlantee',
        errors,
        formData: { username, email }
      });
    }

    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      username,
      email,
      password
    });

    req.session.token = response.data.access_token;
    
    const userResponse = await axios.get(`${API_BASE_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${response.data.access_token}`
      }
    });
    
    req.session.user = userResponse.data;
    
    res.redirect('/dashboard');
    
  } catch (error) {
    let errors = ['Registration failed. Please try again.'];
    
    if (error.response && error.response.data) {
      if (error.response.data.detail) {
        if (typeof error.response.data.detail === 'string') {
          errors = [error.response.data.detail];
        } else if (Array.isArray(error.response.data.detail)) {
          errors = error.response.data.detail.map(err => err.msg || err);
        }
      }
    }
    
    res.render('auth/register', {
      title: 'Sign Up - BePlantee',
      errors,
      formData: { username: req.body.username, email: req.body.email }
    });
  }
});

router.get('/login', (req, res) => {
  if (req.session.user) {
    return res.redirect('/dashboard');
  }
  
  const successMessage = req.session.successMessage || null;
  req.session.successMessage = null; 
  
  res.render('auth/login', {
    title: 'Login - BePlantee',
    errors: null,
    success: successMessage,
    formData: {}
  });
});

router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    const response = await axios.post(`${API_BASE_URL}/auth/login`, 
      new URLSearchParams({
        username,
        password
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );

    req.session.token = response.data.access_token;
    
    try {
      const userResponse = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${response.data.access_token}`
        }
      });
      req.session.user = userResponse.data;
    } catch (e) {
      req.session.user = { username };
    }
    
    res.redirect('/dashboard');
    
  } catch (error) {
    let errors = ['Invalid username or password'];
    
    if (error.response && error.response.data && error.response.data.detail) {
      errors = [error.response.data.detail];
    }
    
    res.render('auth/login', {
      title: 'Login - BePlantee',
      errors,
      success: null,
      formData: { username: req.body.username }
    });  
  }
});

router.get('/forgot-password', (req, res) => {
  if (req.session.user) {
    return res.redirect('/dashboard');
  }
  res.render('auth/email-verification', {
    title: 'Reset Password - BePlantee',
    errors: null
  });
});

router.post('/verify-email', async (req, res) => {
  try {
    const { email, repeat_email } = req.body;
    
    if (!email || !email.includes('@')) {
      return res.render('auth/email-verification', {
        title: 'Reset Password - BePlantee',
        errors: ['Please enter a valid email address']
      });
    }
    
    if (email !== repeat_email) {
      return res.render('auth/email-verification', {
        title: 'Reset Password - BePlantee',
        errors: ['Email addresses do not match']
      });
    }

    const response = await axios.post(`${API_BASE_URL}/password-reset/verify-email`, {
      email
    });

    res.redirect(`/auth/reset-password?email=${encodeURIComponent(email)}`);
    
  } catch (error) {
    let errors = ['Email not found in our database'];
    
    if (error.response && error.response.data && error.response.data.detail) {
      errors = [error.response.data.detail];
    }
    
    res.render('auth/email-verification', {
      title: 'Reset Password - BePlantee',
      errors
    });
  }
});

router.get('/reset-password', (req, res) => {
  if (req.session.user) {
    return res.redirect('/dashboard');
  }
  
  const email = req.query.email;
  if (!email) {
    return res.redirect('/auth/forgot-password');
  }
  
  res.render('auth/reset-password', {
    title: 'Reset Password - BePlantee',
    errors: null,
    email: email
  });
});

router.post('/reset-password', async (req, res) => {
  try {
    const { email, password, repeat_password } = req.body;
    
    if (password !== repeat_password) {
      return res.render('auth/reset-password', {
        title: 'Reset Password - BePlantee',
        errors: ['Passwords do not match'],
        email: email
      });
    }
    
    if (password.length < 8) {
      return res.render('auth/reset-password', {
        title: 'Reset Password - BePlantee',
        errors: ['Password must be at least 8 characters long'],
        email: email
      });
    }
    
    const response = await axios.post(`${API_BASE_URL}/password-reset/reset`, {
      email,
      password
    });

    req.session.successMessage = 'Password has been reset successfully! You can now log in with your new password.';
    res.redirect('/auth/login');
    
  } catch (error) {
    let errors = ['Failed to reset password'];
    
    if (error.response && error.response.data) {
      if (error.response.data.detail) {
        if (typeof error.response.data.detail === 'string') {
          errors = [error.response.data.detail];
        } else if (Array.isArray(error.response.data.detail)) {
          errors = error.response.data.detail.map(err => err.msg || err);
        }
      }
    }
    
    res.render('auth/reset-password', {
      title: 'Reset Password - BePlantee',
      errors,
      email: req.body.email
    });
  }
});

router.get('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error('Session destroy error:', err);
    }
    res.redirect('/');
  });
});

module.exports = router;