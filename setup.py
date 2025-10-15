#!/usr/bin/env python3
"""
Setup script for Biogen Patient Services Streamlit App
"""

import os
import sys

def create_secrets_file():
    """Create secrets.toml file with OpenAI API key"""
    
    print("🔧 Setting up Biogen Patient Services App...")
    
    # Check if .streamlit directory exists
    streamlit_dir = ".streamlit"
    if not os.path.exists(streamlit_dir):
        os.makedirs(streamlit_dir)
        print(f"✅ Created {streamlit_dir} directory")
    
    # Check for existing secrets file
    secrets_file = os.path.join(streamlit_dir, "secrets.toml")
    
    if os.path.exists(secrets_file):
        print(f"⚠️  {secrets_file} already exists")
        response = input("Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Get OpenAI API key
    print("\n🔑 OpenAI API Key Configuration:")
    print("Get your API key from: https://platform.openai.com/api-keys")
    
    api_key = input("Enter your OpenAI API key (sk-proj-...): ").strip()
    
    if not api_key.startswith('sk-proj-'):
        print("⚠️  Warning: API key doesn't start with 'sk-proj-'. Are you sure this is correct?")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Create secrets file
    secrets_content = f"""# Streamlit Secrets Configuration
# This file contains your OpenAI API key

[openai]
api_key = "{api_key}"
"""
    
    try:
        with open(secrets_file, 'w') as f:
            f.write(secrets_content)
        print(f"✅ Created {secrets_file}")
        print("🔒 Your API key has been saved securely")
    except Exception as e:
        print(f"❌ Error creating secrets file: {e}")
        return
    
    print("\n🚀 Setup complete! You can now:")
    print("1. Run locally: streamlit run streamlit_app.py")
    print("2. Deploy to Streamlit Cloud: https://share.streamlit.io/")
    print("3. Follow DEPLOYMENT_GUIDE.md for other platforms")

def check_requirements():
    """Check if required packages are installed"""
    
    required_packages = ['streamlit', 'openai']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("📦 Installing missing packages...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
            return False
    
    return True

def main():
    print("🏥 Biogen Patient Services - Setup Script")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Create secrets file
    create_secrets_file()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run: streamlit run streamlit_app.py")
    print("2. Open: http://localhost:8501")
    print("3. Test your app with real AI responses!")

if __name__ == "__main__":
    main()
