const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

// Demo login endpoints (no real authentication for demo)
router.post('/login', authController.login);
router.post('/logout', authController.logout);
router.get('/me', authController.getCurrentUser);

module.exports = router;
