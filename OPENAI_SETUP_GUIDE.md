# 🔑 OpenAI API Key Setup Guide

## 📋 Quick Setup (2 minutes)

### **Step 1: Get Your OpenAI API Key**
1. Go to: https://platform.openai.com/api-keys
2. Sign in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-`)

### **Step 2: Configure Your API Key**

**Option A: Using the setup script (Easiest)**
```bash
# Run this command with your actual API key
./setup_api_key.sh sk-proj-your-actual-openai-api-key-here
```

**Option B: Manual setup**
```bash
# 1. Create .env file for Node.js
echo "OPENAI_API_KEY=sk-proj-your-actual-key-here" > .env

# 2. Update Streamlit secrets
mkdir -p .streamlit
echo '[openai]' > .streamlit/secrets.toml
echo 'api_key = "sk-proj-your-actual-key-here"' >> .streamlit/secrets.toml
```

### **Step 3: Test Your Setup**
```bash
# Activate virtual environment and test
source venv/bin/activate
python test_openai.py
```

### **Step 4: Run Your App**
```bash
# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
streamlit run streamlit_app.py
```

---

## 🧪 Testing Your Integration

### **Test Script Results**
When you run `python test_openai.py`, you should see:
```
✅ API key found: sk-proj-...
✅ OpenAI package available
✅ API test successful!
Response: Hello! API key is working correctly.
✅ Streamlit package available
✅ Streamlit secrets file found
✅ API key found in secrets file

🎉 All tests passed! Your integration is ready!
```

### **Manual Test**
1. **Start the app**: `streamlit run streamlit_app.py`
2. **Open**: http://localhost:8501
3. **Login as Patient or Agent**
4. **Use AI chat** - you should get real OpenAI responses, not demo mode

---

## 🚀 Deployment with API Key

### **Streamlit Cloud (Recommended)**
1. **Upload to GitHub** with your files
2. **Go to**: https://share.streamlit.io/
3. **Deploy from GitHub**
4. **In app settings**, add secret:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: `sk-proj-your-actual-key-here`

### **Other Platforms**
- **Railway**: Add environment variable `OPENAI_API_KEY`
- **Render**: Add environment variable `OPENAI_API_KEY`
- **Heroku**: Add config var `OPENAI_API_KEY`

---

## 🔧 Troubleshooting

### **"API key not found"**
```bash
# Check if .env file exists
ls -la .env

# Check if secrets file exists
ls -la .streamlit/secrets.toml

# Manually set environment variable
export OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### **"API test failed"**
1. **Check API key format** - should start with `sk-proj-`
2. **Check OpenAI account credits** - need sufficient balance
3. **Check network connectivity**
4. **Verify API key permissions**

### **"Streamlit not working"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Check if packages are installed
pip list | grep streamlit
pip list | grep openai

# Reinstall if needed
pip install streamlit openai python-dotenv
```

---

## 📱 What You'll Get

### **Real AI Integration**
- ✅ **GPT-4 responses** instead of hardcoded text
- ✅ **Context-aware** conversations
- ✅ **Patient-specific** information
- ✅ **Professional medical** responses
- ✅ **Emotional support** capabilities

### **App Features**
- ✅ **Patient Dashboard** - Treatment journey, AI chat
- ✅ **Agent Dashboard** - Patient queue, metrics, AI testing
- ✅ **Real-time Chat** - Instant AI responses
- ✅ **Mobile Responsive** - Works on all devices
- ✅ **Professional UI** - Healthcare-focused design

---

## 🎯 Success Indicators

### **Working Correctly**
- AI responses are unique and contextual
- Patient gets personalized responses
- Agent can test different scenarios
- No "demo mode" messages
- Responses are natural and helpful

### **Still in Demo Mode**
- Generic, hardcoded responses
- Same response for different questions
- "Demo mode" indicators in UI
- No personalization

---

## 🆘 Need Help?

### **Common Issues**
1. **API key format**: Must start with `sk-proj-`
2. **Environment variables**: Must be set correctly
3. **Virtual environment**: Must be activated
4. **Network**: Must have internet connection
5. **Credits**: OpenAI account must have balance

### **Quick Fixes**
```bash
# Re-run setup
./setup_api_key.sh sk-proj-your-actual-key-here

# Test again
source venv/bin/activate && python test_openai.py

# Start app
source venv/bin/activate && streamlit run streamlit_app.py
```

---

## 🎉 You're Ready!

Once setup is complete:
1. **Your app has real AI integration**
2. **External users get professional experience**
3. **No hardcoded responses**
4. **Context-aware conversations**
5. **Ready for deployment**

**Your Biogen Patient Services app is now powered by real OpenAI AI!** 🚀
