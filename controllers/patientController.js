class PatientController {
  
  // Get patient data
  async getPatientData(req, res) {
    try {
      const { patientId } = req.params;
      
      // Demo patient data
      const patientData = {
        id: patientId,
        name: 'Sarah Parker',
        diagnosis: 'Relapsing-Remitting MS',
        therapy: 'Tysabri',
        diagnosisDate: 'October 20, 2025',
        nextInfusion: 'October 25, 2025',
        location: 'Palo Alto, CA',
        status: 'Active',
        adherence: 95,
        satisfaction: 92,
        riskFactors: ['High anxiety', 'New diagnosis'],
        lastInteraction: new Date().toISOString(),
        totalInteractions: 8,
        sentimentTrend: '+15%'
      };

      res.json({ patient: patientData });
    } catch (error) {
      console.error('Get patient data error:', error);
      res.status(500).json({ error: 'Failed to get patient data' });
    }
  }

  // Get patient schedule
  async getPatientSchedule(req, res) {
    try {
      const { patientId } = req.params;
      
      // Demo schedule data
      const schedule = {
        patientId,
        nextAppointment: {
          date: '2025-10-25',
          time: '10:00 AM',
          location: 'Stanford Health Care',
          type: 'Tysabri Infusion',
          duration: '2 hours'
        },
        upcomingAppointments: [
          {
            date: '2025-11-22',
            time: '2:00 PM',
            location: 'Palo Alto Medical Foundation',
            type: 'Tysabri Infusion'
          },
          {
            date: '2025-12-20',
            time: '11:00 AM',
            location: 'Stanford Health Care',
            type: 'Tysabri Infusion'
          }
        ],
        annualSchedule: [
          '2025-10-25', '2025-11-22', '2025-12-20',
          '2026-01-17', '2026-02-14', '2026-03-14',
          '2026-04-11', '2026-05-09', '2026-06-06',
          '2026-07-04', '2026-08-01', '2026-08-29',
          '2026-09-26', '2026-10-24'
        ]
      };

      res.json({ schedule });
    } catch (error) {
      console.error('Get patient schedule error:', error);
      res.status(500).json({ error: 'Failed to get patient schedule' });
    }
  }

  // Update patient information
  async updatePatient(req, res) {
    try {
      const { patientId } = req.params;
      const updates = req.body;
      
      // In a real app, this would update the database
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

  // Get patient interactions history
  async getPatientInteractions(req, res) {
    try {
      const { patientId } = req.params;
      
      // Demo interaction history
      const interactions = [
        {
          id: 'int_001',
          date: '2025-10-20',
          type: 'Initial Diagnosis Call',
          duration: '45 minutes',
          sentiment: 'High Anxiety',
          topics: ['MS education', 'treatment options', 'anxiety management'],
          agent: 'Dr. Sarah Chen'
        },
        {
          id: 'int_002',
          date: '2025-10-21',
          type: 'Welcome Call',
          duration: '30 minutes',
          sentiment: 'Medium Anxiety',
          topics: ['treatment plan', 'appointment scheduling', 'support resources'],
          agent: 'Cindy Smith'
        },
        {
          id: 'int_003',
          date: '2025-10-22',
          type: 'AI Chat',
          duration: '15 minutes',
          sentiment: 'Positive',
          topics: ['side effects', 'appointment questions', 'transportation'],
          agent: 'AI Assistant'
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
