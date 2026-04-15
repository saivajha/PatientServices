const express = require('express');
const router = express.Router();
const naturosageController = require('../controllers/naturosageController');

router.get('/sources', (req, res) => naturosageController.getSourceStatus(req, res));
router.post('/assessment/start', (req, res) => naturosageController.startAssessment(req, res));
router.post('/assessment/constitution', (req, res) => naturosageController.submitConstitution(req, res));
router.post('/assessment/symptoms', (req, res) => naturosageController.submitSymptoms(req, res));
router.get('/assessment/:sessionId', (req, res) => naturosageController.getSession(req, res));

module.exports = router;
