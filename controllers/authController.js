const jwt = require('jsonwebtoken');

class AuthController {

  async login(req, res) {
    try {
      const { role } = req.body;

      const demoUsers = {
        patient: {
          id: 'patient_001',
          name: 'Ravi Sharma',
          role: 'patient',
          email: 'ravi.sharma@example.com',
          age: 42,
          gender: 'Male',
          chiefComplaint: 'Chronic digestive issues',
          location: 'New Delhi, India'
        },
        practitioner: {
          id: 'practitioner_001',
          name: 'Dr. Meera Joshi',
          role: 'practitioner',
          email: 'dr.meera@naturosage.com',
          department: 'Homeopathic Medicine',
          experience: '12 years',
          specializations: ['Constitutional Prescribing', 'Chronic Disease Management', 'Pediatric Homeopathy']
        }
      };

      if (!role || !demoUsers[role]) {
        return res.status(400).json({ error: 'Invalid role. Use "patient" or "practitioner"' });
      }

      const user = demoUsers[role];

      const token = jwt.sign(
        {
          userId: user.id,
          role: user.role,
          name: user.name
        },
        process.env.JWT_SECRET || 'demo-secret-key',
        { expiresIn: '24h' }
      );

      res.json({
        success: true,
        token,
        user: {
          id: user.id,
          name: user.name,
          role: user.role,
          email: user.email,
          ...user
        }
      });

    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({ error: 'Login failed' });
    }
  }

  async logout(req, res) {
    res.json({ success: true, message: 'Logged out successfully' });
  }

  async getCurrentUser(req, res) {
    try {
      const user = req.user || {
        id: 'demo_user',
        name: 'Demo User',
        role: 'demo'
      };
      res.json({ user });
    } catch (error) {
      console.error('Get current user error:', error);
      res.status(500).json({ error: 'Failed to get user info' });
    }
  }
}

module.exports = new AuthController();
