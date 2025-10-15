import streamlit as st
import openai
import os
from datetime import datetime
import json
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="Patient Services",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Biogen brand colors and elegant styling
st.markdown("""
<style>
    /* Import Biogen font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main header with Biogen blue gradient */
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #0066cc 50%, #0080ff 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 102, 204, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Patient card with elegant blue gradient */
    .user-card {
        background: linear-gradient(135deg, #e6f3ff 0%, #cce7ff 50%, #b3d9ff 100%);
        padding: 2rem;
        border-radius: 15px;
        color: #003366;
        margin-bottom: 1.5rem;
        border-left: 5px solid #0066cc;
        box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
    }
    
    .user-card h2 {
        color: #003366;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Agent card with professional green gradient */
    .agent-card {
        background: linear-gradient(135deg, #f0f8f0 0%, #e0f0e0 50%, #d0e8d0 100%);
        padding: 2rem;
        border-radius: 15px;
        color: #2d5a2d;
        margin-bottom: 1.5rem;
        border-left: 5px solid #4a7c4a;
        box-shadow: 0 4px 16px rgba(74, 124, 74, 0.1);
    }
    
    .agent-card h2 {
        color: #2d5a2d;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Chat messages with Biogen styling */
    .chat-message {
        padding: 1.25rem;
        border-radius: 15px;
        margin: 0.75rem 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .user-message {
        background: linear-gradient(135deg, #0066cc 0%, #0080ff 100%);
        color: white;
        margin-left: 25%;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        color: #333;
        margin-right: 25%;
        border: 2px solid #e6f3ff;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.1);
    }
    
    /* Metric cards with Biogen styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 102, 204, 0.1);
        text-align: center;
        margin: 0.75rem;
        border: 1px solid #e6f3ff;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 102, 204, 0.15);
    }
    
    .metric-card h3 {
        color: #0066cc;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-card p {
        color: #666;
        font-weight: 500;
        margin: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #0066cc 0%, #0080ff 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border: 2px solid #e6f3ff;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        border: 2px solid #e6f3ff;
        border-radius: 10px;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #4a7c4a;
        border-radius: 10px;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #dc3545;
        border-radius: 10px;
    }
    
    /* Journey tracker styling */
    .journey-step {
        background: linear-gradient(135deg, #e6f3ff 0%, #f0f8ff 100%);
        border: 2px solid #0066cc;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Quick action buttons */
    .quick-action {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 2px solid #e6f3ff;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .quick-action:hover {
        border-color: #0066cc;
        background: linear-gradient(135deg, #e6f3ff 0%, #f0f8ff 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 102, 204, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
def init_openai():
    # Try to get API key from environment variable first
    api_key = os.getenv('OPENAI_API_KEY')
    
    # If not found in environment, try Streamlit secrets
    if not api_key:
        try:
            api_key = st.secrets['openai']['api_key']
        except:
            pass
    
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable or configure it in Streamlit secrets.")
        return None
    
    try:
        # Test the API key with a simple call
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        # Don't make an actual API call here, just validate the key format
        if not api_key.startswith('sk-proj-'):
            st.error("⚠️ Invalid API key format. Please check your OpenAI API key.")
            return None
        return True
    except Exception as e:
        st.error(f"Error initializing OpenAI: {e}")
        return None

# Initialize session state
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'openai_initialized' not in st.session_state:
    st.session_state.openai_initialized = False

# Patient context data
PATIENT_CONTEXT = {
    "name": "Sarah Parker",
    "role": "patient",
    "diagnosis": "Relapsing-Remitting MS",
    "therapy": "Tysabri",
    "diagnosisDate": "October 20, 2025",
    "nextInfusion": "October 25, 2025",
    "location": "Palo Alto, CA"
}

AGENT_CONTEXT = {
    "name": "Cindy Smith",
    "role": "agent",
    "department": "Patient Services",
    "experience": "5 years",
    "specializations": ["MS Treatment", "Tysabri Support", "Patient Education"]
}

# AI Response Generation
def generate_ai_response(message, user_context, provider="openai"):
    """Generate AI response using OpenAI or fallback to demo mode"""
    
    # Try OpenAI first if available
    if provider == "openai" and init_openai():
        try:
            # Get API key from environment or secrets
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                try:
                    api_key = st.secrets['openai']['api_key']
                except:
                    return generate_demo_response(message, user_context)
            
            system_prompt = f"""You are an AI assistant for Biogen Patient Services, specifically helping patients with Multiple Sclerosis (MS) who are on Tysabri therapy. You are empathetic, knowledgeable, and supportive.

Patient Context:
- Name: {user_context['name']}
- Role: {user_context['role']}
- Diagnosis: {user_context.get('diagnosis', 'Relapsing-Remitting MS')}
- Therapy: {user_context.get('therapy', 'Tysabri')}
- Diagnosis Date: {user_context.get('diagnosisDate', 'October 20, 2025')}
- Next Infusion: {user_context.get('nextInfusion', 'October 25, 2025')}
- Location: {user_context.get('location', 'Palo Alto, CA')}
- Current Date: {datetime.now().strftime('%B %d, %Y')}

Your role is to:
1. Answer questions about MS, Tysabri treatment, side effects, appointments, and lifestyle
2. Provide emotional support and reassurance
3. Help with practical matters like transportation, insurance, and scheduling
4. Be conversational and natural, like a knowledgeable friend who happens to be an expert
5. Always prioritize patient safety and recommend contacting healthcare providers for medical concerns
6. Keep responses concise but helpful (2-4 sentences typically)

Important guidelines:
- Be warm and empathetic
- Use the patient's name naturally in conversation
- Don't provide specific medical advice - refer to healthcare providers for that
- Be encouraging about treatment and prognosis
- Offer practical help when possible
- If you don't know something, admit it and suggest who might know"""

            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.warning(f"OpenAI API error: {e}. Using demo mode instead.")
            return generate_demo_response(message, user_context)
    
    # Fallback to demo mode
    return generate_demo_response(message, user_context)

def generate_demo_response(message, user_context):
    """Generate demo response for when OpenAI is not available"""
    user_name = user_context['name'].split(' ')[0]
    lower_message = message.lower().strip()
    
    # Personal questions
    if 'what is my name' in lower_message or 'my name' in lower_message:
        return f"Your name is {user_context['name']}. I'm here to help you with your Tysabri treatment journey."
    
    if 'who am i' in lower_message:
        return f"I'm talking to {user_context['name']}. You're a patient starting Tysabri treatment for MS. How can I help you today?"
    
    # Medical questions
    if 'what is tysabri' in lower_message or 'tysabri' in lower_message:
        return f"Tysabri (natalizumab) is a medication used to treat relapsing-remitting multiple sclerosis. It's given as an IV infusion every 28 days and helps reduce MS inflammation and relapses. You'll be starting this treatment on October 25, 2025. Do you have any specific questions about how it works?"
    
    if 'side effects' in lower_message:
        return f"Common side effects of Tysabri can include headache, fatigue, nausea, and sometimes mild flu-like symptoms, especially in the first few infusions. Most people tolerate it well, and side effects usually improve over time. Your healthcare team will monitor you closely for any concerns. Are you worried about any particular side effects?"
    
    if 'headache' in lower_message:
        return f"Headaches can happen with Tysabri, especially after infusions. You can usually take acetaminophen (Tylenol) for relief. Stay hydrated and rest in a cool, dark room if needed. Most infusion-related headaches improve within 24-48 hours. Is this something you're experiencing?"
    
    # Appointment questions
    if 'appointment' in lower_message or 'when is my infusion' in lower_message:
        return f"Your next infusion is scheduled for October 25, 2025. After that, you'll have infusions every 28 days. I can help you schedule future appointments or reschedule if needed. Would you like me to help you with anything specific about your appointment?"
    
    # Transportation
    if 'transportation' in lower_message or 'ride' in lower_message:
        return f"I can help you arrange transportation to your appointments! We can coordinate Uber or Lyft rides, medical transportation, or help you coordinate with family or friends. Just let me know your address and I can set up a ride for your October 25th appointment. Would you like me to help arrange that now?"
    
    # Emotional support
    if any(word in lower_message for word in ['worried', 'anxious', 'scared', 'nervous']):
        return f"It's completely normal to feel worried or anxious about starting a new treatment, especially with a new MS diagnosis. Many people feel this way. Tysabri is a very effective treatment, and your healthcare team will monitor you closely. You're taking the right steps by getting treatment early. Is there something specific that's worrying you? I'm here to listen and help."
    
    # Greetings
    if any(word in lower_message for word in ['hello', 'hi', 'hey']):
        return f"Hello {user_name}! I'm your AI assistant for your Tysabri treatment journey. I can help you with questions about MS, your treatment, appointments, side effects, or anything else you're curious about. What would you like to know?"
    
    if 'thank you' in lower_message or 'thanks' in lower_message:
        return f"You're very welcome, {user_name}! I'm glad I could help. Is there anything else you'd like to know about your treatment or MS?"
    
    # General fallback
    if any(word in lower_message for word in ['?', 'what', 'how', 'why', 'when', 'where']):
        return f"That's a great question, {user_name}. I want to make sure I give you the most accurate and helpful information. Could you provide a bit more detail about what specifically you'd like to know? I can help with questions about MS, Tysabri treatment, appointments, side effects, lifestyle, family, work, or any other concerns you might have."
    
    # Final fallback
    return f"I understand you're asking about \"{message}\", {user_name}. I'm your AI assistant for your Tysabri treatment journey. I can help you with questions about MS, your medication, appointments, side effects, lifestyle, family, work, or anything else on your mind. Could you tell me more about what you'd like to know? I'm here to support you."

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Patient Services</h1>
        <p>AI powered Patient Support System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Section
    if st.session_state.user_role is None:
        st.markdown("### 👋 Welcome! Please choose your role to continue:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👤 Login as Patient (Sarah Parker)", use_container_width=True):
                st.session_state.user_role = "patient"
                st.session_state.user_name = PATIENT_CONTEXT["name"]
                st.session_state.chat_history = []
                st.rerun()
        
        with col2:
            if st.button("👩‍💼 Login as Agent (Cindy Smith)", use_container_width=True):
                st.session_state.user_role = "agent"
                st.session_state.user_name = AGENT_CONTEXT["name"]
                st.session_state.chat_history = []
                st.rerun()
    
    else:
        # User is logged in
        user_context = PATIENT_CONTEXT if st.session_state.user_role == "patient" else AGENT_CONTEXT
        
        # Sidebar
        with st.sidebar:
            st.markdown(f"""
            <div class="{'user-card' if st.session_state.user_role == 'patient' else 'agent-card'}">
                <h3>👋 Welcome, {st.session_state.user_name}!</h3>
                <p><strong>Role:</strong> {st.session_state.user_role.title()}</p>
                {f'<p><strong>Diagnosis:</strong> {user_context["diagnosis"]}</p>' if st.session_state.user_role == "patient" else ''}
                {f'<p><strong>Department:</strong> {user_context["department"]}</p>' if st.session_state.user_role == "agent" else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # AI Configuration
            st.markdown("### 🤖 AI Configuration")
            ai_provider = st.selectbox(
                "Choose AI Provider",
                ["openai", "demo"],
                help="OpenAI requires API key, Demo works without"
            )
            
            # Test AI Connection
            if st.button("🔍 Test AI Connection"):
                test_message = "Hello, are you working?"
                with st.spinner("Testing AI connection..."):
                    response = generate_ai_response(test_message, user_context, ai_provider)
                st.success(f"✅ AI Response: {response}")
            
            # Logout
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user_role = None
                st.session_state.user_name = None
                st.session_state.chat_history = []
                st.rerun()
        
        # Main Content
        if st.session_state.user_role == "patient":
            show_patient_dashboard(user_context)
        else:
            show_agent_dashboard(user_context)

def show_patient_dashboard(user_context):
    """Display patient dashboard"""
    
    # Welcome Section
    st.markdown(f"""
    <div class="user-card">
        <h2>Welcome back, {user_context['name'].split(' ')[0]}!</h2>
        <p><strong>Diagnosis:</strong> {user_context['diagnosis']} • <strong>Therapy:</strong> {user_context['therapy']}</p>
        <p>Your next infusion is scheduled for <strong>{user_context['nextInfusion']}</strong>. We're here to support you every step of the way.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Treatment Journey
    st.markdown("### 🗺️ Your Treatment Journey")
    
    journey_col1, journey_col2, journey_col3 = st.columns(3)
    
    with journey_col1:
        st.markdown("""
        <div class="journey-step">
            <h4 style="color: #0066cc; font-weight: 600; margin-bottom: 0.5rem;">✅ MS Diagnosis</h4>
            <p style="color: #666; margin: 0; font-size: 0.9rem;">October 20, 2025</p>
        </div>
        """, unsafe_allow_html=True)
    
    with journey_col2:
        st.markdown("""
        <div class="journey-step">
            <h4 style="color: #0066cc; font-weight: 600; margin-bottom: 0.5rem;">✅ Treatment Plan</h4>
            <p style="color: #666; margin: 0; font-size: 0.9rem;">Tysabri Approved</p>
        </div>
        """, unsafe_allow_html=True)
    
    with journey_col3:
        st.markdown("""
        <div class="journey-step">
            <h4 style="color: #0066cc; font-weight: 600; margin-bottom: 0.5rem;">📅 First Infusion</h4>
            <p style="color: #666; margin: 0; font-size: 0.9rem;">October 25, 2025</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Chat Section
    st.markdown("### 💬 AI Support Chat")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>AI:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask me anything about MS, Tysabri, appointments, or your treatment:", placeholder="e.g., What is Tysabri?")
    
    if st.button("Send Message", use_container_width=True):
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })
            
            # Generate AI response
            with st.spinner("AI is thinking..."):
                ai_response = generate_ai_response(user_input, user_context)
            
            # Add AI response to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now()
            })
            
            st.rerun()
    
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Contact Your Rep", use_container_width=True):
            # Get patient phone number
            patient_phone = st.text_input("Enter your phone number (e.g., +15551234567):", key="patient_phone", placeholder="+1 555 123-4567")
            if patient_phone:
                # Create WhatsApp message
                message = f"Hi Cindy! This is Sarah Parker (Patient ID: SP-2025-001). I have some questions about my Tysabri therapy. My number is {patient_phone}. Thank you for your support! 💙"
                encoded_message = urllib.parse.quote(message)
                agent_number = "+15559876543"  # Cindy's number
                whatsapp_url = f"https://wa.me/{agent_number.replace('+', '').replace('-', '').replace(' ', '')}?text={encoded_message}"
                
                # Create a clickable link
                st.markdown(f"""
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{whatsapp_url}" target="_blank" style="
                        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                        color: white;
                        padding: 12px 24px;
                        text-decoration: none;
                        border-radius: 25px;
                        font-weight: 600;
                        display: inline-block;
                        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
                    ">
                        💬 Open WhatsApp Chat
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ WhatsApp link generated! Click the button above to start chatting with Cindy.")
            else:
                st.info("Please enter your phone number to generate the WhatsApp link.")
    
    with col2:
        if st.button("🚗 Request Transportation", use_container_width=True):
            st.success("Transportation assistance feature would help arrange rides to your appointments.")
    
    with col3:
        if st.button("📅 Schedule Appointment", use_container_width=True):
            st.success("Appointment scheduling feature would help you manage your infusion appointments.")

def show_agent_dashboard(user_context):
    """Display agent dashboard"""
    
    # Welcome Section
    st.markdown(f"""
    <div class="agent-card">
        <h2>Welcome back, {user_context['name'].split(' ')[0]}!</h2>
        <p><strong>Department:</strong> {user_context['department']} • <strong>Experience:</strong> {user_context['experience']}</p>
        <p>You have <strong>3 active patients</strong> today. AI is handling routine questions while you focus on complex cases.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    st.markdown("### 📊 Dashboard Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0066cc; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">12</h3>
            <p style="color: #666; font-weight: 500; margin: 0; font-size: 1rem;">Active Patients</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #4a7c4a; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">8</h3>
            <p style="color: #666; font-weight: 500; margin: 0; font-size: 1rem;">Calls Today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #ff6b35; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">2</h3>
            <p style="color: #666; font-weight: 500; margin: 0; font-size: 1rem;">Pending Prior Auths</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #28a745; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">92%</h3>
            <p style="color: #666; font-weight: 500; margin: 0; font-size: 1rem;">Satisfaction Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Patient Queue
    st.markdown("### 👥 Active Patients")
    
    patient_data = {
        "Sarah Parker": {
            "status": "High Priority",
            "next_appointment": "Oct 25, 2025",
            "last_contact": "Oct 21, 2025",
            "concerns": ["New diagnosis anxiety", "Treatment expectations"]
        },
        "John Smith": {
            "status": "Medium Priority", 
            "next_appointment": "Nov 15, 2025",
            "last_contact": "Oct 20, 2025",
            "concerns": ["Insurance coverage", "Side effects"]
        },
        "Maria Garcia": {
            "status": "Low Priority",
            "next_appointment": "Nov 22, 2025", 
            "last_contact": "Oct 19, 2025",
            "concerns": ["Transportation", "Work accommodations"]
        }
    }
    
    for patient, info in patient_data.items():
        with st.expander(f"👤 {patient} - {info['status']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Next Appointment:** {info['next_appointment']}")
                st.write(f"**Last Contact:** {info['last_contact']}")
            with col2:
                st.write(f"**Key Concerns:** {', '.join(info['concerns'])}")
            
            # WhatsApp contact button
            st.markdown("---")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(f"📞 Contact {patient.split()[0]}", key=f"contact_{patient}"):
                    # Get patient phone number
                    phone_input = st.text_input(f"Enter {patient}'s phone number:", key=f"phone_{patient}", placeholder="+1 555 123-4567")
                    if phone_input:
                        # Create WhatsApp message
                        message = f"Hi {patient.split()[0]}! This is Cindy from Biogen Patient Services. I'm calling to check on your Tysabri treatment. How are you feeling today? We're here to support you every step of the way! 💙"
                        encoded_message = urllib.parse.quote(message)
                        patient_number = phone_input.replace('+', '').replace('-', '').replace(' ', '')
                        whatsapp_url = f"https://wa.me/{patient_number}?text={encoded_message}"
                        
                        st.markdown(f"""
                        <div style="text-align: center; margin: 10px 0;">
                            <a href="{whatsapp_url}" target="_blank" style="
                                background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                                color: white;
                                padding: 10px 20px;
                                text-decoration: none;
                                border-radius: 20px;
                                font-weight: 600;
                                display: inline-block;
                                box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
                                font-size: 14px;
                            ">
                                💬 Open WhatsApp Chat
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.success("✅ WhatsApp link generated! Click the button above to start chatting.")
                    else:
                        st.info("Please enter the patient's phone number to generate the WhatsApp link.")
            
            with col_btn2:
                if st.button(f"📋 View Details", key=f"details_{patient}"):
                    st.info(f"Detailed patient information for {patient} would be displayed here in a real system.")
    
    # AI Testing Section
    st.markdown("### 🤖 AI Testing & Support")
    
    # Test different scenarios
    test_scenarios = [
        "What is my name?",
        "Tell me about Tysabri side effects",
        "I'm feeling anxious about my treatment",
        "Can you help with transportation?",
        "When is my next appointment?"
    ]
    
    st.markdown("**Quick Test Scenarios:**")
    for scenario in test_scenarios:
        if st.button(f"Test: {scenario}", key=f"test_{scenario}"):
            with st.spinner("AI is responding..."):
                response = generate_ai_response(scenario, PATIENT_CONTEXT)
            st.success(f"**Response:** {response}")

if __name__ == "__main__":
    main()
