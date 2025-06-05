const express = require('express');
const axios = require('axios');
const router = express.Router();

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

router.get('/', async (req, res) => {
  try {
    const searchQuery = req.query.search || '';
    const page = parseInt(req.query.page) || 1;
    const limit = 20;
    const offset = (page - 1) * limit;
    
    let apiUrl = `${API_BASE_URL}/plant-types/`;
    
    if (searchQuery) {
      apiUrl += `search?query=${encodeURIComponent(searchQuery)}`;
    }
    
    const response = await axios.get(apiUrl);
    const allPlantTypes = response.data.plant_types || [];
    
    const totalItems = allPlantTypes.length;
    const totalPages = Math.ceil(totalItems / limit);
    const plantTypes = allPlantTypes.slice(offset, offset + limit);
    
    const pagination = {
      currentPage: page,
      totalPages: totalPages,
      totalItems: totalItems,
      hasNext: page < totalPages,
      hasPrev: page > 1,
      nextPage: page < totalPages ? page + 1 : null,
      prevPage: page > 1 ? page - 1 : null,
      pages: []
    };
    
    const startPage = Math.max(1, page - 2);
    const endPage = Math.min(totalPages, page + 2);
    
    for (let i = startPage; i <= endPage; i++) {
      pagination.pages.push({
        number: i,
        isCurrent: i === page,
        url: buildPageUrl(req, i)
      });
    }
    
    res.render('plant-types/index', {
      title: 'Plant Types - BePlantee',
      plantTypes: plantTypes,
      searchQuery: searchQuery,
      pagination: pagination,
      isAuthenticated: !!req.session.user,
      user: req.session.user,
      showHeader: false,
      showFooter: false,
      error: null
    });
  } catch (error) {
    console.error('Error fetching plant types:', error);
    res.render('plant-types/index', {
      title: 'Plant Types - BePlantee', 
      plantTypes: [],
      searchQuery: req.query.search || '',
      pagination: { currentPage: 1, totalPages: 0, totalItems: 0, hasNext: false, hasPrev: false, pages: [] },
      isAuthenticated: !!req.session.user,
      user: req.session.user,
      showHeader: false,
      showFooter: false,
      error: 'Unable to load plant types'
    });
  }
});

function buildPageUrl(req, page) {
  const url = new URL(req.originalUrl, `http://${req.get('host')}`);
  url.searchParams.set('page', page);
  return url.pathname + url.search;
}

router.get('/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/plants/${req.params.id}`);
    
    res.render('plant-types/show', {
      title: `${response.data.common_name || response.data.scientific_name} - BePlantee`,
      plant: response.data,
      isAuthenticated: !!req.session.user,
      user: req.session.user,
      showHeader: false,
      showFooter: false
    });
  } catch (error) {
    console.error('Error fetching plant type:', error);
    res.status(404).render('error', {
      title: 'Plant Type Not Found',
      message: 'The plant type you are looking for could not be found.',
      error: { status: 404 }
    });
  }
});

module.exports = router;