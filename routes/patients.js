const express = require('express');
const router = express.Router();
const patientController = require('../controllers/patientController');
const authMiddleware = require('../middleware/auth');

router.get('/data/:patientId', authMiddleware, (req, res) => patientController.getPatientData(req, res));
router.get('/schedule/:patientId', authMiddleware, (req, res) => patientController.getPatientSchedule(req, res));
router.put('/update/:patientId', authMiddleware, (req, res) => patientController.updatePatient(req, res));
router.get('/interactions/:patientId', authMiddleware, (req, res) => patientController.getPatientInteractions(req, res));

module.exports = router;
