#!/bin/bash

echo "🚀 Patient Services - Streamlit Cloud Deployment Helper"
echo "======================================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please run this from your PatientServices directory."
    exit 1
fi

echo ""
echo "📋 Follow these steps to deploy your app to Streamlit Cloud:"
echo ""

echo "1️⃣ CREATE GITHUB REPOSITORY"
echo "   • Go to: https://github.com/new"
echo "   • Repository name: patient-services-app (or your choice)"
echo "   • Make it PUBLIC (required for free Streamlit Cloud)"
echo "   • Click 'Create repository'"
echo ""

read -p "Press Enter when you've created the GitHub repository..."

echo ""
echo "2️⃣ ADD GITHUB REMOTE AND PUSH"
echo "   • Replace 'YOUR_USERNAME' with your GitHub username below:"
echo ""

# Get current directory name as suggested repo name
CURRENT_DIR=$(basename "$PWD")
echo "Suggested commands:"
echo "git remote add origin https://github.com/YOUR_USERNAME/$CURRENT_DIR.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""

read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

echo ""
echo "🔄 Adding GitHub remote and pushing code..."

# Add remote and push
git remote add origin https://github.com/$GITHUB_USERNAME/$CURRENT_DIR.git
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Code pushed to GitHub successfully!"
    echo ""
    echo "3️⃣ DEPLOY TO STREAMLIT CLOUD"
    echo "   • Go to: https://share.streamlit.io/"
    echo "   • Sign in with GitHub"
    echo "   • Click 'New app'"
    echo "   • Select repository: $CURRENT_DIR"
    echo "   • Main file: streamlit_app.py"
    echo "   • App URL: patient-services-demo (or your choice)"
    echo "   • Click 'Deploy!'"
    echo ""
    echo "4️⃣ CONFIGURE API KEY"
    echo "   • In Streamlit Cloud dashboard, go to Settings > Secrets"
    echo "   • Add this content:"
    echo ""
    echo "[openai]"
    echo "api_key = \"YOUR_OPENAI_API_KEY_HERE\""
    echo ""
    echo "🎉 Your app will be live at: https://patient-services-demo.streamlit.app/"
    echo ""
    echo "📱 Share this URL with anyone to test your AI-powered Patient Services app!"
else
    echo "❌ Failed to push to GitHub. Please check your repository URL and try again."
fi
