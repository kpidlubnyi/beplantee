const axios = require('axios');

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

async function validateToken(req, res, next) {
  if (!req.session.token) {
    return next();
  }

  try {
    const response = await axios.get(`${API_BASE_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${req.session.token}`
      },
      timeout: 5000 
    });

    req.session.user = response.data;
    next();
  } catch (error) {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      console.log('Invalid token, clearing session');
      req.session.destroy((err) => {
        if (err) {
          console.error('Session destroy error:', err);
        }
      });
    }
    next();
  }
}

function requireAuth(req, res, next) {
  if (!req.session.user || !req.session.token) {
    req.session.returnTo = req.originalUrl;
    return res.redirect('/auth/login');
  }
  next();
}

function redirectIfAuthenticated(req, res, next) {
  if (req.session.user && req.session.token) {
    return res.redirect('/dashboard');
  }
  next();
}

module.exports = {
  validateToken,
  requireAuth,
  redirectIfAuthenticated
};