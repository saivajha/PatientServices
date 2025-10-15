#!/usr/bin/env python3
"""
Test OpenAI API Key Integration
"""

import os
import sys

def test_openai_integration():
    """Test OpenAI API key integration"""
    
    print("🧪 Testing OpenAI API Integration")
    print("=" * 40)
    
    # Check if API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        print("\nTo set it:")
        print("export OPENAI_API_KEY='sk-proj-your-actual-key-here'")
        print("\nOr add it to your .env file")
        return False
    
    if not api_key.startswith('sk-proj-'):
        print("⚠️  API key doesn't start with 'sk-proj-'")
        print(f"Current key: {api_key[:10]}...")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test OpenAI integration
    try:
        from openai import OpenAI
        print("✅ OpenAI package available")
        
        client = OpenAI(api_key=api_key)
        
        print("🔄 Testing API call...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for Biogen Patient Services."},
                {"role": "user", "content": "Say 'Hello! API key is working correctly.'"}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ API test successful!")
        print(f"Response: {result}")
        
        return True
        
    except ImportError:
        print("❌ OpenAI package not installed")
        print("Install it with: pip install openai")
        return False
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. Insufficient credits in OpenAI account")
        print("3. Network connectivity issues")
        return False

def test_streamlit_integration():
    """Test Streamlit app integration"""
    
    print("\n🔄 Testing Streamlit Integration")
    print("=" * 40)
    
    try:
        import streamlit
        print("✅ Streamlit package available")
        
        # Check if secrets file exists
        secrets_file = ".streamlit/secrets.toml"
        if os.path.exists(secrets_file):
            print("✅ Streamlit secrets file found")
            
            with open(secrets_file, 'r') as f:
                content = f.read()
                if 'sk-proj-' in content:
                    print("✅ API key found in secrets file")
                else:
                    print("⚠️  API key not found in secrets file")
                    print("Update .streamlit/secrets.toml with your API key")
        else:
            print("⚠️  Streamlit secrets file not found")
            print("Create .streamlit/secrets.toml with your API key")
        
        return True
        
    except ImportError:
        print("❌ Streamlit package not installed")
        print("Install it with: pip install streamlit")
        return False

def main():
    print("🏥 Biogen Patient Services - OpenAI Integration Test")
    print("=" * 60)
    
    # Test OpenAI
    openai_ok = test_openai_integration()
    
    # Test Streamlit
    streamlit_ok = test_streamlit_integration()
    
    print("\n" + "=" * 60)
    print("📋 Test Results:")
    print(f"OpenAI Integration: {'✅ PASS' if openai_ok else '❌ FAIL'}")
    print(f"Streamlit Integration: {'✅ PASS' if streamlit_ok else '❌ FAIL'}")
    
    if openai_ok and streamlit_ok:
        print("\n🎉 All tests passed! Your integration is ready!")
        print("\n🚀 You can now run:")
        print("streamlit run streamlit_app.py")
        print("\nYour app will have real AI responses!")
    else:
        print("\n🔧 Please fix the issues above before running the app.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
