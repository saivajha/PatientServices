const jwt = require('jsonwebtoken');

// Demo authentication middleware
const authMiddleware = (req, res, next) => {
  try {
    // For demo purposes, we'll create a mock user if no token is provided
    const authHeader = req.headers.authorization;
    
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      
      try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET || 'demo-secret-key');
        req.user = {
          id: decoded.userId,
          name: decoded.name,
          role: decoded.role
        };
      } catch (jwtError) {
        // Invalid token, but we'll continue with demo user
        console.warn('Invalid JWT token:', jwtError.message);
      }
    }
    
    // If no valid user from token, create demo user
    if (!req.user) {
      req.user = {
        id: 'demo_user',
        name: 'Demo User',
        role: 'demo'
      };
    }
    
    next();
  } catch (error) {
    console.error('Auth middleware error:', error);
    
    // Even if auth fails, continue with demo user
    req.user = {
      id: 'demo_user',
      name: 'Demo User',
      role: 'demo'
    };
    
    next();
  }
};

module.exports = authMiddleware;
