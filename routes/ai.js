const express = require('express');
const router = express.Router();
const aiController = require('../controllers/aiController');
const authMiddleware = require('../middleware/auth');

// AI Chat endpoint
router.post('/chat', authMiddleware, aiController.generateResponse);

// Get available LLM providers
router.get('/providers', aiController.getProviders);

// Test AI connection
router.get('/test', authMiddleware, aiController.testConnection);

module.exports = router;
