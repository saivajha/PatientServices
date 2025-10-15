#!/usr/bin/env python3
"""
Test OpenAI API integration specifically for Streamlit
"""

import os
import sys

def test_streamlit_api():
    """Test API key access in Streamlit context"""
    
    print("🧪 Testing Streamlit OpenAI Integration")
    print("=" * 50)
    
    # Test environment variable
    env_key = os.getenv('OPENAI_API_KEY')
    print(f"Environment API Key: {'✅ Found' if env_key else '❌ Not found'}")
    if env_key:
        print(f"  Key: {env_key[:10]}...")
    
    # Test secrets file
    try:
        import streamlit as st
        secrets_key = st.secrets['openai']['api_key']
        print(f"Streamlit Secrets API Key: ✅ Found")
        print(f"  Key: {secrets_key[:10]}...")
    except Exception as e:
        print(f"Streamlit Secrets API Key: ❌ Not found - {e}")
    
    # Test actual API call
    try:
        from openai import OpenAI
        
        # Try environment key first
        api_key = env_key
        if not api_key:
            try:
                api_key = st.secrets['openai']['api_key']
            except:
                pass
        
        if not api_key:
            print("❌ No API key available for testing")
            return False
        
        print(f"\n🔄 Testing API call with key: {api_key[:10]}...")
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "Say 'Streamlit API test successful!'"}
            ],
            max_tokens=20
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ API Test Successful!")
        print(f"Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        return False

if __name__ == "__main__":
    test_streamlit_api()
