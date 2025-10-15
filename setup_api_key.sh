#!/bin/bash

echo "🔧 Biogen Patient Services - API Key Setup"
echo "=========================================="

# Check if API key is provided as argument
if [ $# -eq 0 ]; then
    echo "❌ Please provide your OpenAI API key as an argument"
    echo "Usage: ./setup_api_key.sh sk-proj-YOUR ACTUAL API KEY HERE"
    exit 1
fi

API_KEY=$1

# Validate API key format
if [[ ! $API_KEY == sk-proj-* ]]; then
    echo "⚠️  Warning: API key doesn't start with 'sk-proj-'"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Setup cancelled"
        exit 1
    fi
fi

echo "✅ API key format validated: ${API_KEY:0:10}..."

# Create .env file for Node.js
echo "📝 Creating .env file for Node.js..."
cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=$API_KEY

# Server Configuration
PORT=3000
NODE_ENV=development

# JWT Secret
JWT_SECRET=biogen-patient-services-jwt-secret-2025

# CORS Configuration
CORS_ORIGIN=http://localhost:3000

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
EOF

echo "✅ Created .env file"

# Update Streamlit secrets
echo "📝 Updating Streamlit secrets..."
mkdir -p .streamlit

cat > .streamlit/secrets.toml << EOF
# Streamlit Secrets Configuration
[openai]
api_key = "$API_KEY"
EOF

echo "✅ Updated .streamlit/secrets.toml"

# Set environment variable for current session
export OPENAI_API_KEY=$API_KEY

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 You can now run:"
echo "1. Streamlit app: source venv/bin/activate && streamlit run streamlit_app.py"
echo "2. Node.js app: npm install && npm run dev"
echo ""
echo "🔍 Test your setup:"
echo "source venv/bin/activate && python test_openai.py"
echo ""
echo "Your API key is configured for both apps!"
