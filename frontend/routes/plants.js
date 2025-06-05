const express = require('express');
const axios = require('axios');
const multer = require('multer');
const FormData = require('form-data');
const router = express.Router();

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024, 
  },
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'), false);
    }
  }
});

function requireAuth(req, res, next) {
  if (!req.session.user || !req.session.token) {
    return res.redirect('/auth/login');
  }
  next();
}

router.get('/', requireAuth, async (req, res) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/user-plants/`, {
      headers: {
        'Authorization': `Bearer ${req.session.token}`
      }
    });

    res.render('plants/index', {
      title: 'My Plants - BePlantee',
      plants: response.data,
      user: req.session.user
    });
  } catch (error) {
    console.error('Error fetching plants:', error);
    
    if (error.response && error.response.status === 401) {
      req.session.destroy();
      return res.redirect('/auth/login');
    }
    
    res.render('plants/index', {
      title: 'My Plants - BePlantee',
      plants: [],
      user: req.session.user,
      error: 'Unable to load your plants'
    });
  }
});

router.get('/add', requireAuth, async (req, res) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/plants/dropdown-options`);
    
    res.render('plants/add', {
      title: 'Add Plant - BePlantee',
      plantTypes: response.data,
      user: req.session.user
    });
  } catch (error) {
    console.error('Error fetching plant types:', error);
    
    if (error.response && error.response.status === 401) {
      req.session.destroy();
      return res.redirect('/auth/login');
    }
    
    res.render('plants/add', {
      title: 'Add Plant - BePlantee',
      plantTypes: [],
      user: req.session.user,
      error: 'Unable to load plant types'
    });
  }
});

router.post('/add', requireAuth, upload.single('image'), async (req, res) => {
  try {
    console.log('Request body:', req.body);
    console.log('Request file:', req.file);

    const { plant_id, name } = req.body;

    if (!plant_id || !name) {
      throw new Error('Plant ID and name are required');
    }

    if (name.length > 20) {
      throw new Error('Plant name cannot exceed 20 characters');
    }

    const formData = new FormData();
    formData.append('plant_id', plant_id);
    formData.append('name', name);
    
    if (req.file) {
      formData.append('file', req.file.buffer, {
        filename: req.file.originalname,
        contentType: req.file.mimetype
      });
    }

    const response = await axios.post(
      `${API_BASE_URL}/user-plants/create-with-form`,
      formData,
      {
        headers: {
          'Authorization': `Bearer ${req.session.token}`,
          ...formData.getHeaders()
        }
      }
    );

    console.log('Plant created successfully:', response.data);

    res.redirect('/plants');
    
  } catch (error) {
    console.error('Error adding plant:', error);
    
    if (error.response && error.response.status === 401) {
      req.session.destroy();
      return res.redirect('/auth/login');
    }
    
    let errorMessage = 'Failed to add plant. Please try again.';
    
    if (error.response && error.response.data) {
      if (error.response.data.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map(err => err.msg || err.message || err).join(', ');
        }
      }
    } else if (error.message) {
      errorMessage = error.message;
    }
    
    try {
      const typesResponse = await axios.get(`${API_BASE_URL}/plants/dropdown-options`);
      res.render('plants/add', {
        title: 'Add Plant - BePlantee',
        plantTypes: typesResponse.data,
        user: req.session.user,
        error: errorMessage,
        formData: req.body
      });
    } catch (typesError) {
      res.render('plants/add', {
        title: 'Add Plant - BePlantee',
        plantTypes: [],
        user: req.session.user,
        error: errorMessage,
        formData: req.body
      });
    }
  }
});

router.get('/:id', requireAuth, async (req, res) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/user-plants/${req.params.id}`, {
      headers: {
        'Authorization': `Bearer ${req.session.token}`
      }
    });

    res.render('plants/show', {
      title: `${response.data.name} - BePlantee`,
      plant: response.data,
      user: req.session.user
    });
  } catch (error) {
    console.error('Error fetching plant:', error);
    
    if (error.response && error.response.status === 401) {
      req.session.destroy();
      return res.redirect('/auth/login');
    }
    
    res.status(404).render('error', {
      title: 'Plant Not Found',
      message: 'The plant you are looking for could not be found.',
      error: { status: 404 }
    });
  }
});

router.post('/:id/water', requireAuth, async (req, res) => {
  try {
    await axios.post(`${API_BASE_URL}/user-plants/${req.params.id}/water`, {}, {
      headers: {
        'Authorization': `Bearer ${req.session.token}`
      }
    });

    res.json({ success: true, message: 'Plant watered successfully!' });
  } catch (error) {
    console.error('Error watering plant:', error);
    
    if (error.response && error.response.status === 401) {
      return res.status(401).json({ success: false, message: 'Authentication required' });
    }
    
    res.status(500).json({ success: false, message: 'Failed to water plant' });
  }
});

router.post('/:id/sunfill', requireAuth, async (req, res) => {
  try {
    await axios.post(`${API_BASE_URL}/user-plants/${req.params.id}/sunfill`, {}, {
      headers: {
        'Authorization': `Bearer ${req.session.token}`
      }
    });

    res.json({ success: true, message: 'Sunlight recorded successfully!' });
  } catch (error) {
    console.error('Error recording sunlight:', error);
    
    if (error.response && error.response.status === 401) {
      return res.status(401).json({ success: false, message: 'Authentication required' });
    }
    
    res.status(500).json({ success: false, message: 'Failed to record sunlight' });
  }
});

router.delete('/:id', requireAuth, async (req, res) => {
  try {
    await axios.delete(`${API_BASE_URL}/user-plants/${req.params.id}`, {
      headers: {
        'Authorization': `Bearer ${req.session.token}`
      }
    });

    res.json({ success: true, message: 'Plant deleted successfully!' });
  } catch (error) {
    console.error('Error deleting plant:', error);
    
    if (error.response && error.response.status === 401) {
      return res.status(401).json({ success: false, message: 'Authentication required' });
    }
    
    res.status(500).json({ success: false, message: 'Failed to delete plant' });
  }
});

router.get('/:id/edit', requireAuth, async (req, res) => {
  try {
    const plantResponse = await axios.get(`${API_BASE_URL}/user-plants/${req.params.id}`, {
      headers: {
        'Authorization': `Bearer ${req.session.token}`
      }
    });

    const typesResponse = await axios.get(`${API_BASE_URL}/plants/dropdown-options`);
    
    res.render('plants/edit', {
      title: `Edit ${plantResponse.data.name} - BePlantee`,
      plant: plantResponse.data,
      plantTypes: typesResponse.data,
      user: req.session.user
    });
  } catch (error) {
    console.error('Error fetching plant for edit:', error);
    
    if (error.response && error.response.status === 401) {
      req.session.destroy();
      return res.redirect('/auth/login');
    }
    
    res.status(404).render('error', {
      title: 'Plant Not Found',
      message: 'The plant you are looking for could not be found.',
      error: { status: 404 }
    });
  }
});

router.post('/:id', requireAuth, upload.single('image'), async (req, res) => {
  return handlePlantUpdate(req, res);
});

router.put('/:id', requireAuth, upload.single('image'), async (req, res) => {
  return handlePlantUpdate(req, res);
});

router.patch('/:id', requireAuth, upload.single('image'), async (req, res) => {
  return handlePlantUpdate(req, res);
});

async function handlePlantUpdate(req, res) {
  try {
    const { name, plant_id, remove_image } = req.body;
    
    console.log('Update request:', { name, plant_id, remove_image, hasFile: !!req.file });
    
    const formData = new FormData();
    
    if (name) formData.append('name', name);
    if (plant_id) formData.append('plant_id', plant_id);
    
    if (remove_image === 'true') {
      console.log('Removing plant image...');
      try {
        await axios.delete(`${API_BASE_URL}/user-plants/${req.params.id}/image`, {
          headers: {
            'Authorization': `Bearer ${req.session.token}`
          }
        });
        console.log('Image removed successfully');
      } catch (imageError) {
        console.log('Image removal failed, but continuing with update:', imageError.message);
      }
    }
    
    if (req.file) {
      console.log('Adding new image file:', req.file.originalname);
      formData.append('file', req.file.buffer, {
        filename: req.file.originalname,
        contentType: req.file.mimetype
      });
    }

    console.log('Sending update request to backend...');
    const response = await axios.patch(
      `${API_BASE_URL}/user-plants/${req.params.id}`,
      formData,
      {
        headers: {
          'Authorization': `Bearer ${req.session.token}`,
          ...formData.getHeaders()
        }
      }
    );

    console.log('Plant updated successfully:', response.data);
    
    res.redirect(`/plants/${req.params.id}`);
    
  } catch (error) {
    console.error('Error updating plant:', error);
    
    if (error.response && error.response.status === 401) {
      req.session.destroy();
      return res.redirect('/auth/login');
    }
    
    let errorMessage = 'Failed to update plant. Please try again.';
    
    if (error.response && error.response.data) {
      if (error.response.data.detail) {
        if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail.map(err => err.msg || err.message || err).join(', ');
        }
      }
    }
    
    try {
      const plantResponse = await axios.get(`${API_BASE_URL}/user-plants/${req.params.id}`, {
        headers: { 'Authorization': `Bearer ${req.session.token}` }
      });
      const typesResponse = await axios.get(`${API_BASE_URL}/plants/dropdown-options`);
      
      res.render('plants/edit', {
        title: `Edit ${plantResponse.data.name} - BePlantee`,
        plant: plantResponse.data,
        plantTypes: typesResponse.data,
        user: req.session.user,
        error: errorMessage,
        formData: req.body
      });
    } catch {
      res.status(500).render('error', {
        title: 'Error',
        message: errorMessage,
        error: { status: 500 }
      });
    }
  }
}

module.exports = router;