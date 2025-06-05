const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.render('pages/home', {
    title: 'BePlantee - Your Digital Garden Companion',
    isAuthenticated: !!req.session.user,
    user: req.session.user,
    showHeader: false,
    showFooter: false  
  });
});

router.get('/dashboard', (req, res) => {
  if (req.session.user && req.session.token) {
    return res.redirect('/plants');
  }
  res.redirect('/auth/login');
});

router.get('/about', (req, res) => {
  res.render('pages/about', {
    title: 'About - BePlantee',
    isAuthenticated: !!req.session.user,
    user: req.session.user,
    showHeader: true,
    showFooter: true
  });
});

router.get('/faq', async (req, res) => {
  try {
    const axios = require('axios');
    const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';
    
    const response = await axios.get(`${API_BASE_URL}/faq`);
    
    res.render('pages/faq', {
      title: 'FAQ - BePlantee',
      faqData: response.data,
      isAuthenticated: !!req.session.user,
      user: req.session.user,
      showHeader: false,
      showFooter: false
    });
  } catch (error) {
    console.error('Error fetching FAQ:', error);
    res.render('pages/faq', {
      title: 'FAQ - BePlantee',
      faqData: { categories: [] },
      isAuthenticated: !!req.session.user,
      user: req.session.user,
      showHeader: false,
      showFooter: false,
      error: 'Unable to load FAQ data'
    });
  }
});

module.exports = router;