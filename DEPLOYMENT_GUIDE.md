# 🚀 Deployment Guide - Biogen Patient Services

## 📋 Overview
This guide will help you deploy your Biogen Patient Services app with integrated OpenAI API key on various free platforms.

## 🎯 Deployment Options

### **Option 1: Streamlit Cloud (Recommended - Easiest)**

#### **Step 1: Prepare Your Repository**
1. **Create a GitHub repository** with your files
2. **Upload all files** to your repository:
   - `streamlit_app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `README.md`

#### **Step 2: Deploy to Streamlit Cloud**
1. **Go to**: https://share.streamlit.io/
2. **Click "Deploy an app"**
3. **Connect your GitHub account**
4. **Select your repository**
5. **Choose main branch and `streamlit_app.py`**
6. **Click "Deploy"**

#### **Step 3: Configure OpenAI API Key**
1. **In your Streamlit Cloud dashboard**
2. **Click on your deployed app**
3. **Go to "Settings" tab**
4. **Add Secret**: `OPENAI_API_KEY`
5. **Value**: Your actual OpenAI API key (`sk-proj-...`)
6. **Click "Save"**

#### **Step 4: Access Your App**
- Your app will be available at: `https://your-app-name.streamlit.app/`
- **Free tier**: Unlimited apps, 1GB RAM, 1 CPU

---

### **Option 2: Railway (Alternative)**

#### **Step 1: Prepare Files**
1. **Create `railway.json`**:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300
  }
}
```

#### **Step 2: Deploy**
1. **Go to**: https://railway.app/
2. **Sign up with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Add environment variable**: `OPENAI_API_KEY`

#### **Step 3: Configure**
- **Free tier**: $5 credit monthly
- **Auto-deploys** on git push

---

### **Option 3: Render (Alternative)**

#### **Step 1: Create `render.yaml`**
```yaml
services:
  - type: web
    name: biogen-patient-services
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: OPENAI_API_KEY
        sync: false
```

#### **Step 2: Deploy**
1. **Go to**: https://render.com/
2. **Connect GitHub**
3. **Create new Web Service**
4. **Select your repository**
5. **Add environment variable**: `OPENAI_API_KEY`

---

### **Option 4: Hugging Face Spaces (Alternative)**

#### **Step 1: Create Space**
1. **Go to**: https://huggingface.co/new-space
2. **Select "Streamlit" SDK**
3. **Create space**

#### **Step 2: Upload Files**
1. **Upload `streamlit_app.py`**
2. **Upload `requirements.txt`**
3. **Upload `.streamlit/config.toml`**

#### **Step 3: Configure Secrets**
1. **Go to Settings tab**
2. **Add Secret**: `OPENAI_API_KEY`
3. **Value**: Your API key

---

## 🔧 Local Testing

### **Before Deployment**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY="sk-proj-your-actual-key-here"

# Run locally
streamlit run streamlit_app.py
```

### **Test Your App**
1. **Open**: http://localhost:8501
2. **Login as Patient or Agent**
3. **Test AI responses**
4. **Verify OpenAI integration**

---

## 🔑 API Key Configuration

### **Method 1: Environment Variables (Recommended)**
```bash
# Local development
export OPENAI_API_KEY="sk-proj-your-actual-key-here"

# Production (set in deployment platform)
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### **Method 2: Streamlit Secrets**
Create `.streamlit/secrets.toml`:
```toml
[openai]
api_key = "sk-proj-your-actual-key-here"
```

---

## 🚀 Quick Start Commands

### **For Streamlit Cloud (Recommended)**
```bash
# 1. Create GitHub repo and upload files
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main

# 2. Go to https://share.streamlit.io/
# 3. Deploy from GitHub
# 4. Add OPENAI_API_KEY in settings
```

### **For Railway**
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway init
railway up

# 3. Set environment variable
railway variables set OPENAI_API_KEY=sk-proj-your-actual-key-here
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] **App loads successfully**
- [ ] **Login works for both Patient and Agent**
- [ ] **AI responses are generated (not demo mode)**
- [ ] **OpenAI API key is working**
- [ ] **Chat functionality works**
- [ ] **Mobile responsive design**
- [ ] **All features accessible**

---

## 🆘 Troubleshooting

### **Common Issues**

**"OpenAI API key not found"**
- Check environment variable is set correctly
- Verify API key format (starts with `sk-proj-`)
- Ensure no extra spaces or quotes

**"App won't deploy"**
- Check `requirements.txt` has correct versions
- Verify `streamlit_app.py` runs locally
- Check deployment platform logs

**"AI responses are generic"**
- Verify OpenAI API key is working
- Check API key has sufficient credits
- Test API key separately

### **Getting Help**
1. **Check deployment platform logs**
2. **Test locally first**
3. **Verify API key works**
4. **Check platform documentation**

---

## 🎉 Success!

Once deployed, your app will be available at:
- **Streamlit Cloud**: `https://your-app-name.streamlit.app/`
- **Railway**: `https://your-app-name.railway.app/`
- **Render**: `https://your-app-name.onrender.com/`
- **Hugging Face**: `https://huggingface.co/spaces/yourusername/your-space`

**Your Biogen Patient Services app is now live with real AI integration!** 🚀
