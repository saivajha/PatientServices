#!/usr/bin/env python3
"""
Configure OpenAI API Key for Biogen Patient Services
"""

import os
import sys

def configure_api_key():
    """Configure OpenAI API key for both Node.js and Streamlit"""
    
    print("🔧 Biogen Patient Services - API Key Configuration")
    print("=" * 60)
    
    # Get OpenAI API key from user
    print("\n🔑 Please enter your OpenAI API key:")
    print("Get it from: https://platform.openai.com/api-keys")
    print("(It should start with 'sk-proj-')")
    
    api_key = input("\nEnter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return False
    
    if not api_key.startswith('sk-proj-'):
        print("⚠️  Warning: API key doesn't start with 'sk-proj-'")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            print("❌ Setup cancelled.")
            return False
    
    print(f"\n✅ API key received: {api_key[:10]}...")
    
    # Configure Node.js .env file
    print("\n📝 Configuring Node.js environment...")
    
    env_content = f"""# OpenAI Configuration
OPENAI_API_KEY={api_key}

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
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file for Node.js")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        print("Please create .env file manually with:")
        print(f"OPENAI_API_KEY={api_key}")
    
    # Configure Streamlit secrets
    print("\n📝 Configuring Streamlit secrets...")
    
    streamlit_dir = ".streamlit"
    if not os.path.exists(streamlit_dir):
        os.makedirs(streamlit_dir)
        print(f"✅ Created {streamlit_dir} directory")
    
    secrets_content = f"""# Streamlit Secrets Configuration
[openai]
api_key = "{api_key}"
"""
    
    try:
        with open(os.path.join(streamlit_dir, 'secrets.toml'), 'w') as f:
            f.write(secrets_content)
        print("✅ Updated .streamlit/secrets.toml")
    except Exception as e:
        print(f"❌ Error updating secrets.toml: {e}")
    
    print("\n🎉 Configuration complete!")
    print("\n🚀 You can now run:")
    print("1. Node.js app: npm install && npm run dev")
    print("2. Streamlit app: streamlit run streamlit_app.py")
    
    print("\n🔍 To test your API key:")
    print("1. Start either app")
    print("2. Login as Patient or Agent")
    print("3. Use AI chat - you should get real OpenAI responses!")
    
    return True

def test_api_key():
    """Test the configured API key"""
    
    print("\n🧪 Testing OpenAI API key...")
    
    try:
        import openai
        
        # Try to load API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No API key found in environment variables")
            return False
        
        openai.api_key = api_key
        
        # Test with a simple request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello, API key is working!'"}],
            max_tokens=20
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ API test successful: {result}")
        return True
        
    except ImportError:
        print("⚠️  OpenAI package not installed. Run: pip install openai")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    if configure_api_key():
        print("\n" + "="*60)
        print("🎯 Next Steps:")
        print("1. Test locally: streamlit run streamlit_app.py")
        print("2. Deploy to Streamlit Cloud: https://share.streamlit.io/")
        print("3. Your app will have real AI responses!")
        print("="*60)
