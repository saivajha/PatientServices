# 🏥 Patient Services - AI Powered Patient Support System

A sophisticated, AI-powered patient support platform designed for Biogen's Tysabri therapy patients with Multiple Sclerosis (MS).

## ✨ Features

### 🤖 **AI-Powered Support**
- **Real OpenAI GPT-4 Integration** - Intelligent, contextual responses
- **Patient-Specific Context** - Personalized conversations
- **Professional Medical Responses** - Healthcare-focused AI assistance
- **Emotional Support** - Empathetic AI interactions

### 👥 **Dual Dashboard System**
- **Patient Dashboard** - Treatment journey, AI chat, appointment management
- **Agent Dashboard** - Patient queue, metrics, AI testing tools
- **Role-Based Access** - Secure login for different user types

### 🎨 **Professional Design**
- **Biogen Brand Colors** - Professional healthcare aesthetic
- **Elegant Typography** - Modern Inter font family
- **Responsive Design** - Works on all devices
- **Smooth Animations** - Professional user experience

### 📊 **Advanced Features**
- **Treatment Journey Tracker** - Visual progress monitoring
- **Real-time Metrics** - Patient and agent performance data
- **WhatsApp Integration** - Direct communication channels
- **Transportation Assistance** - Ride scheduling support

## 🚀 Quick Start

### **For External Users**
Simply visit the deployed app - no setup required!

### **For Local Development**
```bash
# Clone the repository
git clone <your-repo-url>
cd PatientServices

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run streamlit_app.py
```

## 🔧 Configuration

### **API Key Setup**
The app uses OpenAI GPT-4 for intelligent responses. API keys are configured securely through Streamlit Cloud secrets.

### **Environment Variables**
- `OPENAI_API_KEY` - Your OpenAI API key (configured in Streamlit Cloud)

## 📱 User Roles

### **Patient (Sarah Parker)**
- View treatment journey progress
- Chat with AI about MS and Tysabri
- Schedule appointments
- Request transportation
- Contact patient services

### **Agent (Cindy Smith)**
- Monitor patient queue
- View dashboard metrics
- Test AI responses
- Manage patient interactions
- Access comprehensive patient data

## 🎯 Use Cases

### **For Patients**
- **Treatment Education** - Learn about MS and Tysabri therapy
- **Appointment Management** - Schedule and track infusions
- **Emotional Support** - Get encouragement and reassurance
- **Practical Help** - Transportation and logistics assistance

### **For Healthcare Providers**
- **Patient Monitoring** - Track patient progress and satisfaction
- **AI Assistance** - Let AI handle routine questions
- **Performance Metrics** - Monitor call volume and outcomes
- **Quality Assurance** - Test AI responses and patient interactions

## 🛠️ Technical Stack

- **Frontend**: Streamlit (Python web framework)
- **AI**: OpenAI GPT-4 API
- **Styling**: Custom CSS with Biogen branding
- **Deployment**: Streamlit Cloud
- **Security**: Environment variable management

## 📊 Demo Data

The app includes realistic demo data for:
- Patient profiles and treatment histories
- Agent metrics and performance data
- AI conversation examples
- Treatment journey progressions

## 🔒 Security & Privacy

- **Secure API Key Management** - Keys stored in Streamlit Cloud secrets
- **No Data Persistence** - Chat history not stored permanently
- **HIPAA Considerations** - Designed with healthcare privacy in mind
- **Environment Isolation** - Separate development and production environments

## 🎨 Design Philosophy

- **Healthcare-First** - Designed specifically for medical applications
- **User-Centric** - Intuitive interfaces for both patients and providers
- **Professional Aesthetic** - Biogen brand colors and modern typography
- **Accessibility** - Mobile-responsive and accessible design

## 🚀 Deployment

This app is deployed on Streamlit Cloud with:
- **Automatic Updates** - Deploys from GitHub repository
- **Global CDN** - Fast loading worldwide
- **SSL Security** - HTTPS encryption
- **Scalable Infrastructure** - Handles multiple concurrent users

## 📞 Support

For technical support or questions about the Patient Services platform, please contact your Patient Services representative.

---

**Built with ❤️ for Biogen Patient Services**