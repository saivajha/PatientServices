class PatientController {

  async getPatientData(req, res) {
    try {
      const { patientId } = req.params;

      const patientData = {
        id: patientId,
        name: 'Ravi Sharma',
        age: 42,
        gender: 'Male',
        chiefComplaint: 'Chronic digestive issues',
        constitution: 'Lycopodium',
        currentRemedies: ['Lycopodium 200C', 'Nux Vomica 30C'],
        location: 'New Delhi, India',
        status: 'Active',
        improvementScore: 72,
        lastVisit: new Date().toISOString(),
        totalConsultations: 6,
        timeline: [
          { date: '2025-09-01', event: 'First consultation', notes: 'Constitution assessment done' },
          { date: '2025-09-15', event: 'Follow-up', notes: 'Lycopodium 200C prescribed' },
          { date: '2025-10-01', event: 'Progress review', notes: '40% improvement in bloating' }
        ]
      };

      res.json({ patient: patientData });
    } catch (error) {
      console.error('Get patient data error:', error);
      res.status(500).json({ error: 'Failed to get patient data' });
    }
  }

  async getPatientSchedule(req, res) {
    try {
      const { patientId } = req.params;

      const schedule = {
        patientId,
        nextAppointment: {
          date: '2025-11-15',
          time: '10:00 AM',
          location: 'NaturoSage Clinic, New Delhi',
          type: 'Follow-up Consultation',
          duration: '30 minutes'
        },
        upcomingAppointments: [
          { date: '2025-12-15', time: '10:00 AM', location: 'NaturoSage Clinic', type: 'Monthly Follow-up' },
          { date: '2026-01-15', time: '11:00 AM', location: 'NaturoSage Clinic', type: 'Monthly Follow-up' }
        ]
      };

      res.json({ schedule });
    } catch (error) {
      console.error('Get patient schedule error:', error);
      res.status(500).json({ error: 'Failed to get patient schedule' });
    }
  }

  async updatePatient(req, res) {
    try {
      const { patientId } = req.params;
      const updates = req.body;

      res.json({
        success: true,
        message: 'Patient information updated successfully',
        patientId,
        updates
      });
    } catch (error) {
      console.error('Update patient error:', error);
      res.status(500).json({ error: 'Failed to update patient information' });
    }
  }

  async getPatientInteractions(req, res) {
    try {
      const { patientId } = req.params;

      const interactions = [
        {
          id: 'int_001',
          date: '2025-09-01',
          type: 'Initial Consultation',
          duration: '60 minutes',
          notes: 'Constitution assessment: Lycopodium. Chief complaint: chronic bloating and gas worse 4-8 PM.',
          practitioner: 'Dr. Meera Joshi'
        },
        {
          id: 'int_002',
          date: '2025-09-15',
          type: 'Follow-up',
          duration: '30 minutes',
          notes: 'Started Lycopodium 200C. Advised dietary changes — avoid beans, cabbage.',
          practitioner: 'Dr. Meera Joshi'
        },
        {
          id: 'int_003',
          date: '2025-10-01',
          type: 'AI Symptom Check',
          duration: '10 minutes',
          notes: 'Patient used NaturoSage AI to check new symptom: mild headache. Suggested Bryonia 30C as adjunct.',
          practitioner: 'NaturoSage AI'
        }
      ];

      res.json({ interactions });
    } catch (error) {
      console.error('Get patient interactions error:', error);
      res.status(500).json({ error: 'Failed to get patient interactions' });
    }
  }
}

module.exports = new PatientController();
