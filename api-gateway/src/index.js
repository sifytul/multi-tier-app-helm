const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:6000';
const PORT = process.env.PORT || 5000;

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'api-gateway',
    timestamp: new Date().toISOString()
  });
});

// Proxy to backend API
app.get('/api/items', async (req, res) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/items`);
    res.json(response.data);
  } catch (error) {
    res.status(502).json({
      error: 'Backend unavailable',
      details: error.message
    });
  }
});

app.post('/api/items', async (req, res) => {
  try {
    const response = await axios.post(`${BACKEND_URL}/items`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(502).json({
      error: 'Backend unavailable',
      details: error.message
    });
  }
});

app.get('/api/items/:id', async (req, res) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/items/${req.params.id}`);
    res.json(response.data);
  } catch (error) {
    if (error.response?.status === 404) {
      res.status(404).json({ error: 'Item not found' });
    } else {
      res.status(502).json({
        error: 'Backend unavailable',
        details: error.message
      });
    }
  }
});

// Backend health check
app.get('/api/health', async (req, res) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/health`);
    res.json({
      gateway: 'healthy',
      backend: response.data
    });
  } catch (error) {
    res.json({
      gateway: 'healthy',
      backend: 'unavailable'
    });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`API Gateway running on port ${PORT}`);
  console.log(`Backend URL: ${BACKEND_URL}`);
});
