const express = require('express');
const axios = require('axios');
const router = express.Router();

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

function proxyAuth(req, res, next) {
  req.headers.authorization = req.session.token ? `Bearer ${req.session.token}` : '';
  next();
}

router.post('/password-validation', async (req, res) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/password-validation/`,
      req.body.password,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    res.json(response.data);
  } catch (error) {
    console.error('Password validation error:', error);
    res.status(500).json({ errors: ['Validation service unavailable'] });
  }
});

router.get('/plant-types', async (req, res) => {
  try {
    const searchQuery = req.query.search;
    let url = `${API_BASE_URL}/plant-types/`;
    
    if (searchQuery) {
      url += `search?query=${encodeURIComponent(searchQuery)}`;
    }
    
    const response = await axios.get(url);
    res.json(response.data);
  } catch (error) {
    console.error('Plant types fetch error:', error);
    res.status(500).json({ plant_types: [] });
  }
});

router.post('/password-reset/verify-email', async (req, res) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/password-reset/verify-email`,
      req.body
    );
    res.json(response.data);
  } catch (error) {
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      res.status(500).json({ detail: 'Service unavailable' });
    }
  }
});

router.post('/password-reset/reset', async (req, res) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}/password-reset/reset`,
      req.body
    );
    res.json(response.data);
  } catch (error) {
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      res.status(500).json({ detail: 'Service unavailable' });
    }
  }
});

module.exports = router;