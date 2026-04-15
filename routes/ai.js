const express = require('express');
const router = express.Router();
const aiController = require('../controllers/aiController');
const authMiddleware = require('../middleware/auth');

router.post('/chat', authMiddleware, (req, res) => aiController.generateResponse(req, res));
router.get('/providers', (req, res) => aiController.getProviders(req, res));
router.get('/test', authMiddleware, (req, res) => aiController.testConnection(req, res));

module.exports = router;
