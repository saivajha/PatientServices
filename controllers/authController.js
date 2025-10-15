const jwt = require('jsonwebtoken');

class AuthController {
  
  // Demo login (no real authentication for demo purposes)
  async login(req, res) {
    try {
      const { role } = req.body;
      
      // Demo users
      const demoUsers = {
        patient: {
          id: 'patient_001',
          name: 'Sarah Parker',
          role: 'patient',
          email: 'sarah.parker@example.com',
          diagnosis: 'Relapsing-Remitting MS',
          therapy: 'Tysabri',
          diagnosisDate: 'October 20, 2025',
          nextInfusion: 'October 25, 2025',
          location: 'Palo Alto, CA'
        },
        agent: {
          id: 'agent_001',
          name: 'Cindy Smith',
          role: 'agent',
          email: 'cindy.smith@biogen.com',
          department: 'Patient Services',
          experience: '5 years',
          specializations: ['MS Treatment', 'Tysabri Support', 'Patient Education']
        }
      };

      if (!role || !demoUsers[role]) {
        return res.status(400).json({ error: 'Invalid role. Use "patient" or "agent"' });
      }

      const user = demoUsers[role];
      
      // Generate JWT token
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

  // Logout
  async logout(req, res) {
    // In a real app, you might blacklist the token
    res.json({ success: true, message: 'Logged out successfully' });
  }

  // Get current user info
  async getCurrentUser(req, res) {
    try {
      // This would normally extract user from JWT token
      // For demo purposes, we'll return basic info
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
