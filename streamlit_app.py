import streamlit as st
import openai
import os
from datetime import datetime, timedelta
import json
import urllib.parse

# Helper function for generating appointments
def generate_appointments(start_date_str="2025-10-25", count=6):
    """Generate a list of appointment dates spaced 28 days apart"""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    appointments = []
    for i in range(count):
        appointment_date = start_date + timedelta(days=28 * i)
        appointments.append(appointment_date.strftime("%Y-%m-%d"))
    return appointments

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
    
    /* Main header with Biogen blue gradient - Mobile optimized */
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #0066cc 50%, #0080ff 100%);
        padding: 1.5rem 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(0, 102, 204, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        font-size: 1rem;
        font-weight: 300;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem 0.75rem;
            margin-bottom: 0.75rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .main-header p {
            font-size: 0.9rem;
        }
    }
    
    /* Patient card with elegant blue gradient - Compact */
    .user-card {
        background: linear-gradient(135deg, #e6f3ff 0%, #cce7ff 50%, #b3d9ff 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #003366;
        margin-bottom: 0.75rem;
        border-left: 5px solid #0066cc;
        box-shadow: 0 4px 16px rgba(0, 102, 204, 0.1);
    }
    
    .user-card h2 {
        color: #003366;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
    }
    
    /* Agent card with professional green gradient - Compact */
    .agent-card {
        background: linear-gradient(135deg, #f0f8f0 0%, #e0f0e0 50%, #d0e8d0 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #2d5a2d;
        margin-bottom: 0.75rem;
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
        border-radius: 10px;
        padding: 0.75rem;
        margin: 0.5rem 0;
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
    
    /* Mobile-specific improvements */
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
        
        .user-card, .agent-card {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
            margin: 0.5rem;
        }
        
        .journey-step {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .user-message {
            margin-left: 15%;
        }
        
        .ai-message {
            margin-right: 15%;
        }
        
        /* Sidebar improvements for mobile */
        .css-1d391kg {
            padding: 0.5rem;
        }
        
        /* Button improvements for mobile */
        .stButton > button {
            padding: 0.75rem 1rem;
            font-size: 14px;
        }
        
        /* Input improvements for mobile */
        .stTextInput > div > div > input {
            padding: 0.75rem;
            font-size: 16px; /* Prevents zoom on iOS */
        }
        
        /* Date input improvements for mobile */
        .stDateInput > div > div > input {
            padding: 0.75rem;
            font-size: 16px;
        }
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
            # Create proper HTML content
            card_class = 'user-card' if st.session_state.user_role == 'patient' else 'agent-card'
            
            # Build HTML content safely
            html_content = f"""
            <div class="{card_class}">
                <h3>👋 Welcome, {st.session_state.user_name}!</h3>
                <p><strong>Role:</strong> {st.session_state.user_role.title()}</p>"""
            
            if st.session_state.user_role == "patient":
                html_content += f'<p><strong>Diagnosis:</strong> {user_context["diagnosis"]}</p>'
            else:
                html_content += f'<p><strong>Department:</strong> {user_context["department"]}</p>'
            
            html_content += "</div>"
            
            st.markdown(html_content, unsafe_allow_html=True)
            
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
    
    # Welcome Section - Compact
    st.markdown(f"""
    <div class="user-card">
        <h2>Welcome back, {user_context['name'].split(' ')[0]}!</h2>
        <p><strong>{user_context['diagnosis']}</strong> • <strong>{user_context['therapy']}</strong></p>
        <p>Next infusion: <strong>{user_context['nextInfusion']}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Treatment Journey - Compact
    st.markdown("### 🗺️ Treatment Journey")
    
    journey_col1, journey_col2, journey_col3 = st.columns(3)
    
    with journey_col1:
        st.markdown("""
        <div class="journey-step">
            <h5 style="color: #0066cc; font-weight: 600; margin-bottom: 0.5rem; font-size: 1rem;">✅ MS Diagnosis</h5>
            <p style="color: #666; margin: 0; font-size: 0.9rem;">October 20, 2025</p>
        </div>
        """, unsafe_allow_html=True)
    
    with journey_col2:
        st.markdown("""
        <div class="journey-step">
            <h5 style="color: #0066cc; font-weight: 600; margin-bottom: 0.5rem; font-size: 1rem;">✅ Treatment Plan</h5>
            <p style="color: #666; margin: 0; font-size: 0.9rem;">Tysabri Approved</p>
        </div>
        """, unsafe_allow_html=True)
    
    with journey_col3:
        st.markdown("""
        <div class="journey-step">
            <h5 style="color: #0066cc; font-weight: 600; margin-bottom: 0.5rem; font-size: 1rem;">📅 First Infusion</h5>
            <p style="color: #666; margin: 0; font-size: 0.9rem;">October 25, 2025</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Chat Section - Compact
    st.markdown("### 🤖 AI Agent")
    
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
    
    if st.button("Ask Patient Services AI Agent", use_container_width=True):
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
    
    # Quick Actions - Compact
    st.markdown("### 🚀 Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Contact Your Rep", use_container_width=True):
            st.session_state.show_whatsapp = True
        
        if st.session_state.get('show_whatsapp', False):
            col_patient, col_agent = st.columns(2)
            
            with col_patient:
                patient_phone = st.text_input("Your phone number:", key="patient_phone", placeholder="+1 555 123-4567")
            
            with col_agent:
                agent_phone = st.text_input("Agent's phone number:", key="agent_phone", placeholder="+1 555 987-6543", value="+1 555 987-6543")
            
            if patient_phone and agent_phone and len(patient_phone.replace('+', '').replace('-', '').replace(' ', '')) >= 10 and len(agent_phone.replace('+', '').replace('-', '').replace(' ', '')) >= 10:
                # Clean phone numbers
                clean_patient_phone = patient_phone.replace('+', '').replace('-', '').replace(' ', '')
                clean_agent_phone = agent_phone.replace('+', '').replace('-', '').replace(' ', '')
                
                if not clean_patient_phone.startswith('1') and len(clean_patient_phone) == 10:
                    clean_patient_phone = '1' + clean_patient_phone
                if not clean_agent_phone.startswith('1') and len(clean_agent_phone) == 10:
                    clean_agent_phone = '1' + clean_agent_phone
                
                # Create WhatsApp message
                message = f"Hi Cindy! This is Sarah Parker (Patient ID: SP-2025-001). I have some questions about my Tysabri therapy. My number is {patient_phone}. Thank you for your support! 💙"
                encoded_message = urllib.parse.quote(message)
                whatsapp_url = f"https://wa.me/{clean_agent_phone}?text={encoded_message}"
                
                # Create a clickable link that actually works
                st.markdown(f"""
                <div style="text-align: center; margin: 15px 0;">
                    <a href="{whatsapp_url}" target="_blank" style="
                        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                        color: white;
                        padding: 12px 24px;
                        text-decoration: none;
                        border-radius: 25px;
                        font-weight: 600;
                        display: inline-block;
                        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
                        font-size: 16px;
                    ">
                        💬 Open WhatsApp Chat
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ WhatsApp link generated! Click the green button above to start chatting with your agent.")
                st.info(f"📱 This will open WhatsApp and send a message to {agent_phone}")
            elif patient_phone or agent_phone:
                st.error("❌ Please enter valid phone numbers for both fields (at least 10 digits each)")
            else:
                st.info("Please enter both your phone number and the agent's phone number to generate the WhatsApp link.")
    
    with col2:
        if st.button("🚗 Request Transportation", use_container_width=True):
            st.session_state.show_transportation = True
    
    # Transportation Section
    if st.session_state.get('show_transportation', False):
        st.markdown("### 🚗 Transportation Assistance")
        
        # Starting address input
        st.markdown("**Enter your starting address:**")
        starting_address = st.text_input(
            "Your address:",
            placeholder="e.g., 123 Main St, Palo Alto, CA 94301",
            key="starting_address"
        )
        
        if starting_address:
            # Simulate AI finding nearby infusion centers
            st.markdown("**🤖 AI is finding nearby infusion centers...**")
            
            # Simulated infusion centers (in a real app, this would use geocoding APIs)
            nearby_centers = [
                {
                    "name": "Palo Alto Infusion Center",
                    "address": "456 University Ave, Palo Alto, CA 94301",
                    "distance": "2.3 miles",
                    "rating": "4.8",
                    "phone": "(650) 123-4567",
                    "hours": "Mon-Fri 8AM-6PM"
                },
                {
                    "name": "Stanford Medical Center",
                    "address": "300 Pasteur Dr, Stanford, CA 94305",
                    "distance": "3.1 miles", 
                    "rating": "4.9",
                    "phone": "(650) 723-4000",
                    "hours": "Mon-Fri 7AM-7PM"
                },
                {
                    "name": "Mountain View Infusion Clinic",
                    "address": "789 Castro St, Mountain View, CA 94041",
                    "distance": "4.7 miles",
                    "rating": "4.6",
                    "phone": "(650) 987-6543",
                    "hours": "Mon-Fri 9AM-5PM"
                },
                {
                    "name": "Redwood City Medical Center",
                    "address": "123 Veterans Blvd, Redwood City, CA 94063",
                    "distance": "6.2 miles",
                    "rating": "4.7",
                    "phone": "(650) 555-0123",
                    "hours": "Mon-Fri 8AM-6PM"
                }
            ]
            
            st.markdown("**📍 Nearby Infusion Centers:**")
            
            # Display centers with selection
            selected_center = None
            for i, center in enumerate(nearby_centers):
                col_name, col_distance, col_select = st.columns([3, 1, 1])
                
                with col_name:
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #0066cc;">
                        <strong>{center['name']}</strong><br>
                        <small style="color: #666;">{center['address']}</small><br>
                        <small style="color: #666;">⭐ {center['rating']} • 📞 {center['phone']}</small><br>
                        <small style="color: #666;">🕒 {center['hours']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_distance:
                    st.markdown(f"**{center['distance']}**")
                
                with col_select:
                    if st.button(f"Select", key=f"select_center_{i}"):
                        selected_center = center
                        st.session_state.selected_center = center
                        st.success(f"✅ Selected: {center['name']}")
            
            # Uber booking section
            if selected_center or 'selected_center' in st.session_state:
                center = selected_center or st.session_state.selected_center
                
                st.markdown("---")
                st.markdown(f"### 🚗 Book Uber Ride to {center['name']}")
                
                col_from, col_to = st.columns(2)
                
                with col_from:
                    st.markdown(f"**From:** {starting_address}")
                
                with col_to:
                    st.markdown(f"**To:** {center['address']}")
                
                # Trip details
                st.markdown("**Trip Details:**")
                col_distance, col_time, col_price = st.columns(3)
                
                with col_distance:
                    st.metric("Distance", center['distance'])
                
                with col_time:
                    # Simulate estimated time based on distance
                    estimated_time = "8-12 min" if float(center['distance'].split()[0]) < 3 else "12-18 min"
                    st.metric("Est. Time", estimated_time)
                
                with col_price:
                    # Simulate price estimation
                    base_price = 8.50 if float(center['distance'].split()[0]) < 3 else 12.75
                    st.metric("Est. Price", f"${base_price:.2f}")
                
                # Uber booking options
                st.markdown("**Choose Uber Service:**")
                col_uberx, col_comfort, col_xl = st.columns(3)
                
                with col_uberx:
                    if st.button("🚗 UberX", use_container_width=True):
                        uber_url = f"https://m.uber.com/ul/?action=setPickup&pickup[latitude]=37.4419&pickup[longitude]=-122.1430&dropoff[latitude]=37.4419&dropoff[longitude]=-122.1430&dropoff[nickname]={center['name']}"
                        st.markdown(f"""
                        <div style="text-align: center; margin: 15px 0;">
                            <a href="{uber_url}" target="_blank" style="
                                background: linear-gradient(135deg, #000000 0%, #333333 100%);
                                color: white;
                                padding: 12px 24px;
                                text-decoration: none;
                                border-radius: 25px;
                                font-weight: 600;
                                display: inline-block;
                                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                            ">
                                🚗 Open Uber App
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                        st.success("✅ UberX ride requested! The Uber app will open with your trip details.")
                
                with col_comfort:
                    if st.button("🚙 Uber Comfort", use_container_width=True):
                        st.info("💡 Uber Comfort provides newer cars with extra legroom - perfect for medical appointments!")
                
                with col_xl:
                    if st.button("🚐 UberXL", use_container_width=True):
                        st.info("💡 UberXL offers larger vehicles - ideal if you need assistance or extra space!")
                
                # Additional options
                st.markdown("**Additional Options:**")
                col_schedule, col_roundtrip = st.columns(2)
                
                with col_schedule:
                    if st.button("📅 Schedule for Later", use_container_width=True):
                        st.info("💡 Schedule your ride for a specific time - great for planned appointments!")
                
                with col_roundtrip:
                    if st.button("🔄 Round Trip", use_container_width=True):
                        st.info("💡 Book a round trip to ensure you have a ride home after your infusion!")
                
                # Reset selection
                if st.button("🔄 Choose Different Center"):
                    if 'selected_center' in st.session_state:
                        del st.session_state.selected_center
                    st.rerun()
        
        else:
            st.info("📍 Please enter your starting address to find nearby infusion centers.")
    
    with col3:
        if st.button("📅 Schedule Appointment", use_container_width=True):
            st.session_state.show_scheduling = True
    
    # Scheduling Section
    if st.session_state.get('show_scheduling', False):
        st.markdown("### 📅 Infusion Scheduling")
        
        # Initialize appointments if not exists
        if 'appointments' not in st.session_state:
            st.session_state.appointments = generate_appointments()
        
        st.markdown("**Your Next 6 Infusion Appointments (Every 28 Days):**")
        
        # Display appointments with edit capability
        for i, appointment in enumerate(st.session_state.appointments):
            col_date, col_edit, col_status = st.columns([3, 1, 1])
            
            with col_date:
                try:
                    appointment_dt = datetime.strptime(appointment, "%Y-%m-%d")
                    st.write(f"**Appointment {i+1}:** {appointment_dt.strftime('%B %d, %Y')} ({appointment_dt.strftime('%A')})")
                except ValueError:
                    st.write(f"**Appointment {i+1}:** {appointment} (Invalid Date)")
            
            with col_edit:
                if st.button("✏️", key=f"edit_{i}", help="Edit this appointment"):
                    try:
                        st.session_state.edit_appointment = int(i)
                    except (ValueError, TypeError):
                        st.session_state.edit_appointment = 0
            
            with col_status:
                if i == 0:
                    st.success("Next")
                elif i < 3:
                    st.info("Upcoming")
                else:
                    st.write("Scheduled")
        
        # Edit appointment modal
        if 'edit_appointment' in st.session_state and st.session_state.edit_appointment is not None:
            try:
                appointment_index = int(st.session_state.edit_appointment)
                st.markdown("---")
                st.markdown(f"### ✏️ Edit Appointment {appointment_index + 1}")
                
                if appointment_index < len(st.session_state.appointments):
                    current_date = st.session_state.appointments[appointment_index]
                    
                    try:
                        current_date_obj = datetime.strptime(current_date, "%Y-%m-%d").date()
                    except ValueError:
                        # Fallback to a default date if current date is invalid
                        current_date_obj = datetime(2025, 10, 25).date()
                        st.warning(f"⚠️ Invalid date format found: {current_date}. Using default date.")
                else:
                    st.error("❌ Invalid appointment index. Please try again.")
                    st.session_state.edit_appointment = None
                    st.rerun()
                    return
            except (ValueError, TypeError):
                st.error("❌ Invalid appointment selection. Please try again.")
                st.session_state.edit_appointment = None
                st.rerun()
                return
            
            new_date = st.date_input(
                "Select new date:",
                value=current_date_obj,
                key=f"new_date_{appointment_index}",
                help="Select any date. Appointments will adjust to maintain 28-day intervals."
            )
            
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("💾 Save Changes", key="save_appointment"):
                    try:
                        # Calculate new start date
                        new_start = new_date
                        new_appointments = []
                        for i in range(6):
                            appointment_date = new_start + timedelta(days=28 * i)
                            new_appointments.append(appointment_date.strftime("%Y-%m-%d"))
                        
                        st.session_state.appointments = new_appointments
                        st.session_state.edit_appointment = None
                        st.success("✅ Appointments updated! All future appointments adjusted to maintain 28-day intervals.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error updating appointments: {str(e)}")
                        st.info("Please try again or contact support if the issue persists.")
            
            with col_cancel:
                if st.button("❌ Cancel", key="cancel_appointment"):
                    st.session_state.edit_appointment = None
                    st.rerun()
        
        # Custom date selection for extended intervals
        st.markdown("---")
        st.markdown("### 📅 Custom Date Selection")
        st.markdown("**Need to schedule an appointment more than 28 days apart?**")
        
        # Safe date calculation for custom date input
        try:
            if 'appointments' in st.session_state and st.session_state.appointments:
                last_appointment = datetime.strptime(st.session_state.appointments[-1], "%Y-%m-%d").date()
                default_custom_date = last_appointment + timedelta(days=28)
            else:
                # Fallback to a default date if appointments not initialized
                default_custom_date = datetime(2025, 10, 25).date() + timedelta(days=28)
        except (ValueError, KeyError, IndexError):
            # Additional fallback in case of any date parsing issues
            default_custom_date = datetime(2025, 11, 22).date()
        
        custom_date = st.date_input(
            "Select custom date:",
            value=default_custom_date,
            key="custom_date",
            help="This will create a new appointment at your selected date, and subsequent appointments will be 28 days from this date."
        )
        
        if st.button("📅 Schedule Custom Appointment"):
            try:
                # Ensure appointments are initialized
                if 'appointments' not in st.session_state:
                    st.session_state.appointments = generate_appointments()
                
                # Add custom appointment and regenerate future ones
                custom_appointments = []
                for app in st.session_state.appointments:
                    try:
                        app_date = datetime.strptime(app, "%Y-%m-%d").date()
                        if app_date < custom_date:
                            custom_appointments.append(app)
                    except ValueError:
                        # Skip invalid dates
                        continue
                
                custom_appointments.append(custom_date.strftime("%Y-%m-%d"))
                
                # Generate remaining appointments from custom date
                remaining_count = 6 - len(custom_appointments)
                for i in range(remaining_count):
                    next_date = custom_date + timedelta(days=28 * (i + 1))
                    custom_appointments.append(next_date.strftime("%Y-%m-%d"))
                
                st.session_state.appointments = custom_appointments[:6]
                st.success(f"✅ Custom appointment scheduled for {custom_date.strftime('%B %d, %Y')}! Future appointments adjusted.")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error scheduling appointment: {str(e)}")
                st.info("Please try again or contact support if the issue persists.")
        
        # Reset appointments button
        if st.button("🔄 Reset to Default Schedule"):
            st.session_state.appointments = generate_appointments()
            st.success("✅ Appointments reset to default 28-day schedule starting October 25, 2025.")
            st.rerun()

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
                    st.session_state[f'show_agent_whatsapp_{patient}'] = True
            
            if st.session_state.get(f'show_agent_whatsapp_{patient}', False):
                phone_input = st.text_input(f"Enter {patient}'s phone number:", key=f"phone_{patient}", placeholder="+1 555 123-4567")
                if phone_input and len(phone_input.replace('+', '').replace('-', '').replace(' ', '')) >= 10:
                    # Clean phone number
                    clean_phone = phone_input.replace('+', '').replace('-', '').replace(' ', '')
                    if not clean_phone.startswith('1') and len(clean_phone) == 10:
                        clean_phone = '1' + clean_phone
                    
                    # Create WhatsApp message
                    message = f"Hi {patient.split()[0]}! This is Cindy from Biogen Patient Services. I'm calling to check on your Tysabri treatment. How are you feeling today? We're here to support you every step of the way! 💙"
                    encoded_message = urllib.parse.quote(message)
                    whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_message}"
                    
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
                    st.info(f"📱 This will open WhatsApp and send a message to {patient}")
                elif phone_input:
                    st.error("❌ Please enter a valid phone number (at least 10 digits)")
                else:
                    st.info("Please enter the patient's phone number to generate the WhatsApp link.")
            
            with col_btn2:
                if st.button(f"📋 View Details", key=f"details_{patient}"):
                    st.info(f"Detailed patient information for {patient} would be displayed here in a real system.")
    
    # AI Testing Section
    st.markdown("### 🤖 AI Testing & Support")
    
    # Test different scenarios
    test_scenarios = [
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
