const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const methodOverride = require('method-override');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { validateToken } = require('./middleware/auth');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      imgSrc: ["'self'", "data:", "https:", "http:", "blob:"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      scriptSrcAttr: ["'unsafe-inline'"]
    }
  }
}));
app.use(compression());

app.use(cors({
  origin: true,
  credentials: true
}));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(cookieParser());

app.use(methodOverride(function (req, res) {
  if (req.body && typeof req.body === 'object' && '_method' in req.body) {
    const method = req.body._method;
    delete req.body._method;
    return method;
  }
  if (req.query._method) {
    return req.query._method;
  }
}));

app.use(session({
  secret: process.env.SESSION_SECRET || 'beplantee-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    maxAge: 24 * 60 * 60 * 1000,
    httpOnly: true
  }
}));

app.use(express.static(path.join(__dirname, 'public')));

app.use('/uploads', createProxyMiddleware({
  target: API_BASE_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/uploads': '/uploads'
  }
}));

app.use(validateToken);

app.use((req, res, next) => {
  res.locals.user = req.session.user || null;
  res.locals.isAuthenticated = !!req.session.user;
  res.locals.apiBaseUrl = API_BASE_URL;
  next();
});

app.use('/', require('./routes/index'));
app.use('/auth', require('./routes/auth'));
app.use('/plants', require('./routes/plants'));
app.use('/plant-types', require('./routes/plant-types'));
app.use('/api', require('./routes/api'));

app.use((req, res, next) => {
  res.status(404).render('error', {
    title: 'Page Not Found',
    message: 'The page you are looking for could not be found.',
    error: { status: 404 }
  });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  
  if (err.code && err.code.startsWith('LIMIT_')) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).render('plants/add', {
        title: 'Add Plant - BePlantee',
        plantTypes: [],
        user: req.session.user,
        error: 'File size too large. Maximum size is 5MB.',
        formData: req.body
      });
    }
  }
  
  if (err.status === 401 || err.message.includes('Unauthorized')) {
    req.session.destroy((sessionErr) => {
      if (sessionErr) {
        console.error('Session destroy error:', sessionErr);
      }
      res.redirect('/auth/login');
    });
    return;
  }
  
  res.status(err.status || 500).render('error', {
    title: 'Error',
    message: 'Something went wrong!',
    error: process.env.NODE_ENV === 'development' ? err : {}
  });
});

process.on('SIGTERM', () => {
  console.log('🛑 SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('🛑 SIGINT received, shutting down gracefully');
  process.exit(0);
});

app.listen(PORT, () => {
  console.log(`🌱 BePlantee Frontend server is running on port ${PORT}`);
  console.log(`🔗 API Base URL: ${API_BASE_URL}`);
  console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
});

module.exports = app;