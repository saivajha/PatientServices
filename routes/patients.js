const express = require('express');
const router = express.Router();
const patientController = require('../controllers/patientController');
const authMiddleware = require('../middleware/auth');

// Get patient data
router.get('/data/:patientId', authMiddleware, patientController.getPatientData);

// Get patient schedule
router.get('/schedule/:patientId', authMiddleware, patientController.getPatientSchedule);

// Update patient information
router.put('/update/:patientId', authMiddleware, patientController.updatePatient);

// Get patient interactions history
router.get('/interactions/:patientId', authMiddleware, patientController.getPatientInteractions);

module.exports = router;
