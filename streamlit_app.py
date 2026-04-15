import streamlit as st
import openai
import os
from datetime import datetime, timedelta
import json
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="NaturoSage - Homeopathy Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with NaturoSage brand colors (natural greens/earth tones)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #2d5a27 0%, #4a8c3f 50%, #6ab04c 100%);
        padding: 1.5rem 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(74, 140, 63, 0.3);
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

    @media (max-width: 768px) {
        .main-header {
            padding: 1rem 0.75rem;
            margin-bottom: 0.75rem;
        }
        .main-header h1 { font-size: 1.5rem; }
        .main-header p { font-size: 0.9rem; }
    }

    .user-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #1b5e20;
        margin-bottom: 0.75rem;
        border-left: 5px solid #2e7d32;
        box-shadow: 0 4px 16px rgba(46, 125, 50, 0.1);
    }

    .user-card h2, .user-card h3 {
        color: #1b5e20;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
    }

    .practitioner-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 50%, #ffcc80 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #e65100;
        margin-bottom: 0.75rem;
        border-left: 5px solid #ef6c00;
        box-shadow: 0 4px 16px rgba(239, 108, 0, 0.1);
    }

    .practitioner-card h2, .practitioner-card h3 {
        color: #e65100;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .chat-message {
        padding: 1.25rem;
        border-radius: 15px;
        margin: 0.75rem 0;
        font-size: 1rem;
        line-height: 1.6;
    }

    .user-message {
        background: linear-gradient(135deg, #2e7d32 0%, #43a047 100%);
        color: white;
        margin-left: 25%;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
    }

    .ai-message {
        background: linear-gradient(135deg, #f1f8e9 0%, #ffffff 100%);
        color: #333;
        margin-right: 25%;
        border: 2px solid #c8e6c9;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.1);
    }

    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(46, 125, 50, 0.1);
        text-align: center;
        margin: 0.75rem;
        border: 1px solid #e8f5e9;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46, 125, 50, 0.15);
    }

    .metric-card h3 {
        color: #2e7d32;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .metric-card p {
        color: #666;
        font-weight: 500;
        margin: 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2e7d32 0%, #43a047 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
    }

    .stTextInput > div > div > input {
        border: 2px solid #c8e6c9;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: #2e7d32;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
    }

    .constitution-card {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border: 2px solid #9c27b0;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
    }

    .remedy-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border: 2px solid #4caf50;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    .symptom-tag {
        display: inline-block;
        background: #e8f5e9;
        color: #2e7d32;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 2px;
        font-size: 0.85rem;
        border: 1px solid #a5d6a7;
    }

    .diagnosis-box {
        background: linear-gradient(135deg, #fff8e1 0%, #fff3e0 100%);
        border: 2px solid #ff9800;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
    }

    @media (max-width: 768px) {
        .stApp { padding: 0.5rem; }
        .user-card, .practitioner-card { padding: 1rem; margin-bottom: 1rem; }
        .metric-card { padding: 1rem; margin: 0.5rem; }
        .chat-message { padding: 1rem; margin: 0.5rem 0; }
        .user-message { margin-left: 15%; }
        .ai-message { margin-right: 15%; }
        .stButton > button { padding: 0.75rem 1rem; font-size: 14px; }
        .stTextInput > div > div > input { padding: 0.75rem; font-size: 16px; }
    }
</style>
""", unsafe_allow_html=True)

# --- Homeopathic Knowledge Base ---

CONSTITUTIONS = {
    "Calcarea Carbonica": {
        "body_type": "Stocky, tendency to gain weight easily",
        "temperament": "Cautious, methodical, anxious about health",
        "thermal": "Chilly, dislikes cold and damp weather",
        "food_cravings": "Eggs, sweets, cold drinks, starchy food",
        "food_aversions": "Meat, milk (may cause upset)",
        "key_features": ["Sweats easily on head/neck at night", "Slow but steady", "Fear of heights and illness", "Craves routine and security"],
        "color": "#5c6bc0"
    },
    "Phosphorus": {
        "body_type": "Tall, slender, fine-featured",
        "temperament": "Open, sympathetic, sociable, impressionable",
        "thermal": "Warm-blooded but chilly when ill",
        "food_cravings": "Cold drinks, ice cream, salt, spicy food",
        "food_aversions": "Warm food and drinks, fish",
        "key_features": ["Bleeds easily", "Sensitive to light/sound/odors", "Fears thunderstorms and being alone", "Thirsty for cold water"],
        "color": "#ef5350"
    },
    "Sulphur": {
        "body_type": "Lean or round, often stooped posture",
        "temperament": "Intellectual, philosophical, untidy",
        "thermal": "Very warm, aggravated by heat",
        "food_cravings": "Sweets, spicy food, alcohol, fats",
        "food_aversions": "Eggs, milk",
        "key_features": ["Burning sensations", "Skin complaints", "Worse from bathing", "Hot feet at night — sticks feet out of covers"],
        "color": "#ffa726"
    },
    "Lycopodium": {
        "body_type": "Thin upper body, may have bloated abdomen",
        "temperament": "Intellectual but insecure, bossy at home, timid outside",
        "thermal": "Warm but dislikes stuffy rooms",
        "food_cravings": "Warm drinks, sweets, oysters",
        "food_aversions": "Onions, oysters (sometimes), cold food",
        "key_features": ["Right-sided complaints", "Worse 4-8 PM", "Digestive bloating and gas", "Fear of public speaking"],
        "color": "#66bb6a"
    },
    "Natrum Muriaticum": {
        "body_type": "Lean, often pear-shaped",
        "temperament": "Reserved, serious, holds grudges, dislikes consolation",
        "thermal": "Aggravated by sun and heat",
        "food_cravings": "Salt, bread, sour foods",
        "food_aversions": "Slimy food, fat, bread sometimes",
        "key_features": ["Grief and suppressed emotions", "Headaches from sun", "Lips dry and cracked", "Worse from consolation"],
        "color": "#42a5f5"
    },
    "Pulsatilla": {
        "body_type": "Soft, plump, fair complexion",
        "temperament": "Gentle, weepy, changeable moods, craves affection",
        "thermal": "Warm-blooded, worse in warm rooms",
        "food_cravings": "Rich food, butter, cream (but feels worse after)",
        "food_aversions": "Fats, warm food, pork",
        "key_features": ["Symptoms constantly changing", "Better in open air", "Thirstless even with fever", "Weeps easily, wants sympathy"],
        "color": "#ec407a"
    },
    "Nux Vomica": {
        "body_type": "Lean, wiry, tense",
        "temperament": "Driven, competitive, irritable, workaholic",
        "thermal": "Very chilly, sensitive to drafts",
        "food_cravings": "Stimulants (coffee, spicy food, alcohol), rich food",
        "food_aversions": "Food in general when stressed",
        "key_features": ["Digestive issues from overindulgence", "Worse in morning", "Irritable and impatient", "Spasms and cramping"],
        "color": "#8d6e63"
    },
    "Arsenicum Album": {
        "body_type": "Thin, refined, anxious appearance",
        "temperament": "Anxious, restless, fastidious, perfectionist",
        "thermal": "Very chilly, craves warmth",
        "food_cravings": "Warm drinks, sips of water, sour things",
        "food_aversions": "Cold food and drink",
        "key_features": ["Burning pains relieved by warmth", "Restless especially at night (12-2 AM)", "Fear of death and disease", "Wants everything in order"],
        "color": "#78909c"
    }
}

SYMPTOM_CATEGORIES = {
    "Head & Mind": ["Headache", "Migraine", "Vertigo", "Memory issues", "Anxiety", "Depression", "Insomnia", "Brain fog", "Irritability", "Fear/Phobia"],
    "Respiratory": ["Cough (dry)", "Cough (productive)", "Asthma", "Nasal congestion", "Sinusitis", "Sneezing", "Sore throat", "Shortness of breath", "Wheezing"],
    "Digestive": ["Acidity", "Bloating", "Constipation", "Diarrhea", "Nausea", "Vomiting", "Loss of appetite", "Food intolerance", "Heartburn", "Flatulence"],
    "Musculoskeletal": ["Back pain", "Joint pain", "Arthritis", "Muscle cramps", "Stiffness", "Sciatica", "Neck pain", "Rheumatism"],
    "Skin": ["Eczema", "Acne", "Psoriasis", "Urticaria (hives)", "Itching", "Warts", "Hair loss", "Fungal infection", "Dry skin", "Boils"],
    "General": ["Fatigue", "Fever", "Weight gain", "Weight loss", "Weakness", "Swelling", "Burning sensations", "Numbness", "Cold extremities", "Excessive sweating"]
}

HOMEO_MATERIA_MEDICA = {
    "Aconitum Napellus": {
        "common_name": "Monkshood",
        "key_symptoms": ["Sudden onset", "High fever", "Anxiety/fear", "Restlessness", "Dry cough"],
        "modalities": {"worse": "Cold wind, night, fright", "better": "Open air, rest"},
        "potency": "30C",
        "indications": "Sudden acute conditions from cold/fright; panic attacks; early stages of fever/inflammation"
    },
    "Arnica Montana": {
        "common_name": "Leopard's Bane",
        "key_symptoms": ["Trauma/bruising", "Soreness", "Muscle pain", "Fatigue", "Says they are fine when not"],
        "modalities": {"worse": "Touch, motion, damp", "better": "Lying down, rest"},
        "potency": "30C or 200C",
        "indications": "Physical trauma, post-surgery recovery, muscle soreness, overexertion"
    },
    "Belladonna": {
        "common_name": "Deadly Nightshade",
        "key_symptoms": ["Sudden high fever", "Red hot face", "Throbbing headache", "Dilated pupils", "Delirium"],
        "modalities": {"worse": "Light, noise, jarring, afternoon", "better": "Dark room, rest, semi-erect"},
        "potency": "30C",
        "indications": "Acute fever with redness and heat; throbbing headache; sore throat with red tonsils"
    },
    "Bryonia Alba": {
        "common_name": "Wild Hops",
        "key_symptoms": ["Worse from any motion", "Dry mucous membranes", "Thirst for large quantities", "Irritable", "Stitching pains"],
        "modalities": {"worse": "Motion, warmth, morning", "better": "Pressure, rest, cold applications"},
        "potency": "30C",
        "indications": "Dry painful cough; arthritis worse on movement; headache from constipation"
    },
    "Rhus Toxicodendron": {
        "common_name": "Poison Ivy",
        "key_symptoms": ["Restlessness", "Stiffness on first motion", "Better continued motion", "Joint pain", "Skin eruptions with blisters"],
        "modalities": {"worse": "Cold/damp, rest, beginning motion", "better": "Warmth, continued motion, rubbing"},
        "potency": "30C",
        "indications": "Arthritis/joint stiffness; herpes; sprains and strains; restless legs"
    },
    "Nux Vomica": {
        "common_name": "Poison Nut",
        "key_symptoms": ["Digestive complaints", "Irritability", "Oversensitive", "Spasms", "Hangover-like symptoms"],
        "modalities": {"worse": "Morning, cold, stimulants, anger", "better": "Warmth, rest, evening"},
        "potency": "30C",
        "indications": "Digestive disorders from overindulgence; insomnia from mental overwork; constipation with ineffectual urging"
    },
    "Pulsatilla Nigricans": {
        "common_name": "Wind Flower",
        "key_symptoms": ["Changeable symptoms", "Weepy", "Thirstless", "Thick bland discharges", "Craves open air"],
        "modalities": {"worse": "Warm rooms, evening, rich food", "better": "Open air, gentle motion, cold applications"},
        "potency": "30C",
        "indications": "Hormonal issues; shifting pains; ear infections in children; digestive upset from rich food"
    },
    "Sulphur": {
        "common_name": "Brimstone",
        "key_symptoms": ["Burning pains", "Itchy skin worse from heat", "Hot feet at night", "Untidy", "Morning diarrhea"],
        "modalities": {"worse": "Heat, bathing, standing, 11 AM", "better": "Dry warm weather, open air"},
        "potency": "30C or 200C",
        "indications": "Chronic skin conditions; burning sensations; when well-selected remedies fail to act"
    },
    "Arsenicum Album": {
        "common_name": "White Arsenic",
        "key_symptoms": ["Anxiety/restlessness", "Burning pains better from warmth", "Thirst for sips", "Fastidious", "Weakness"],
        "modalities": {"worse": "Cold, midnight to 2 AM, alone", "better": "Warmth, company, hot drinks"},
        "potency": "30C",
        "indications": "Food poisoning; anxiety with restlessness; asthma worse at night; burning diarrhea"
    },
    "Lycopodium Clavatum": {
        "common_name": "Club Moss",
        "key_symptoms": ["Right-sided symptoms", "4-8 PM aggravation", "Bloating after eating", "Lack of confidence", "Craves warm drinks"],
        "modalities": {"worse": "4-8 PM, warm rooms, right side", "better": "Warm drinks, motion, open air"},
        "potency": "30C or 200C",
        "indications": "Digestive disorders with bloating; liver complaints; kidney stones; performance anxiety"
    },
    "Natrum Muriaticum": {
        "common_name": "Table Salt",
        "key_symptoms": ["Grief", "Worse from consolation", "Craves salt", "Sun headache", "Cold sores on lips"],
        "modalities": {"worse": "Sun, heat, consolation, 10 AM", "better": "Open air, cold bathing, sweating"},
        "potency": "200C",
        "indications": "Depression from grief; migraines from sun; chronic sinusitis; eczema at hairline"
    },
    "Calcarea Carbonica": {
        "common_name": "Carbonate of Lime",
        "key_symptoms": ["Sweats on head at night", "Chilly", "Craves eggs", "Slow development", "Anxiety about health"],
        "modalities": {"worse": "Cold/damp, exertion, full moon", "better": "Dry weather, lying on painful side"},
        "potency": "200C",
        "indications": "Slow metabolism; bone/teeth problems; childhood growth issues; recurrent colds"
    },
    "Phosphorus": {
        "common_name": "Phosphorus",
        "key_symptoms": ["Bleeding tendency", "Thirst for cold water", "Sensitive to everything", "Sociable", "Fears thunderstorms"],
        "modalities": {"worse": "Evening, cold, lying on left side", "better": "Cold food/drink, sleep, rubbing"},
        "potency": "30C or 200C",
        "indications": "Nosebleeds; pneumonia; hepatitis; anxiety with desire for company; easy bruising"
    },
    "Ignatia Amara": {
        "common_name": "St. Ignatius Bean",
        "key_symptoms": ["Grief/loss", "Sighing", "Lump in throat", "Contradictory symptoms", "Emotional sensitivity"],
        "modalities": {"worse": "Morning, grief, tobacco, coffee", "better": "Deep breathing, eating, change of position"},
        "potency": "30C or 200C",
        "indications": "Acute grief; emotional shock; nervous headache; hiccough; insomnia from emotional upset"
    },
    "Sepia Officinalis": {
        "common_name": "Cuttlefish Ink",
        "key_symptoms": ["Hormonal imbalance", "Indifference to family", "Bearing-down sensation", "Irritable", "Better from vigorous exercise"],
        "modalities": {"worse": "Cold, before menses, afternoon", "better": "Exercise, warmth, after sleep"},
        "potency": "30C or 200C",
        "indications": "Hormonal disorders; PMS; menopausal symptoms; morning sickness; postpartum depression"
    }
}

SYMPTOM_TO_REMEDIES = {
    "Headache": ["Belladonna", "Bryonia Alba", "Natrum Muriaticum", "Nux Vomica"],
    "Migraine": ["Natrum Muriaticum", "Lycopodium Clavatum", "Phosphorus", "Sepia Officinalis"],
    "Vertigo": ["Phosphorus", "Pulsatilla Nigricans", "Bryonia Alba"],
    "Anxiety": ["Arsenicum Album", "Aconitum Napellus", "Phosphorus", "Calcarea Carbonica"],
    "Depression": ["Natrum Muriaticum", "Ignatia Amara", "Sepia Officinalis", "Sulphur"],
    "Insomnia": ["Nux Vomica", "Arsenicum Album", "Ignatia Amara", "Phosphorus"],
    "Irritability": ["Nux Vomica", "Lycopodium Clavatum", "Sepia Officinalis"],
    "Cough (dry)": ["Aconitum Napellus", "Bryonia Alba", "Phosphorus"],
    "Cough (productive)": ["Pulsatilla Nigricans", "Sulphur", "Calcarea Carbonica"],
    "Asthma": ["Arsenicum Album", "Phosphorus", "Pulsatilla Nigricans"],
    "Nasal congestion": ["Pulsatilla Nigricans", "Natrum Muriaticum", "Calcarea Carbonica"],
    "Sinusitis": ["Natrum Muriaticum", "Pulsatilla Nigricans", "Lycopodium Clavatum"],
    "Sore throat": ["Belladonna", "Lycopodium Clavatum", "Phosphorus"],
    "Acidity": ["Nux Vomica", "Arsenicum Album", "Lycopodium Clavatum"],
    "Bloating": ["Lycopodium Clavatum", "Nux Vomica", "Pulsatilla Nigricans"],
    "Constipation": ["Nux Vomica", "Bryonia Alba", "Sulphur", "Lycopodium Clavatum"],
    "Diarrhea": ["Arsenicum Album", "Phosphorus", "Sulphur"],
    "Nausea": ["Nux Vomica", "Arsenicum Album", "Ignatia Amara", "Sepia Officinalis"],
    "Back pain": ["Rhus Toxicodendron", "Bryonia Alba", "Nux Vomica"],
    "Joint pain": ["Rhus Toxicodendron", "Bryonia Alba", "Calcarea Carbonica"],
    "Arthritis": ["Rhus Toxicodendron", "Bryonia Alba", "Sulphur"],
    "Muscle cramps": ["Nux Vomica", "Rhus Toxicodendron", "Arnica Montana"],
    "Stiffness": ["Rhus Toxicodendron", "Bryonia Alba", "Calcarea Carbonica"],
    "Sciatica": ["Rhus Toxicodendron", "Bryonia Alba", "Lycopodium Clavatum"],
    "Eczema": ["Sulphur", "Natrum Muriaticum", "Arsenicum Album"],
    "Acne": ["Sulphur", "Pulsatilla Nigricans", "Nux Vomica"],
    "Psoriasis": ["Sulphur", "Arsenicum Album", "Lycopodium Clavatum"],
    "Urticaria (hives)": ["Arsenicum Album", "Pulsatilla Nigricans", "Sulphur"],
    "Itching": ["Sulphur", "Arsenicum Album", "Rhus Toxicodendron"],
    "Hair loss": ["Phosphorus", "Natrum Muriaticum", "Lycopodium Clavatum", "Sepia Officinalis"],
    "Fatigue": ["Phosphorus", "Arsenicum Album", "Calcarea Carbonica", "Sepia Officinalis"],
    "Fever": ["Aconitum Napellus", "Belladonna", "Arsenicum Album"],
    "Weight gain": ["Calcarea Carbonica", "Lycopodium Clavatum", "Sulphur"],
    "Weakness": ["Arsenicum Album", "Phosphorus", "Calcarea Carbonica"],
    "Burning sensations": ["Arsenicum Album", "Sulphur", "Phosphorus"],
    "Excessive sweating": ["Calcarea Carbonica", "Phosphorus", "Sulphur"],
    "Fear/Phobia": ["Aconitum Napellus", "Arsenicum Album", "Phosphorus", "Calcarea Carbonica"],
    "Brain fog": ["Lycopodium Clavatum", "Phosphorus", "Calcarea Carbonica"],
    "Memory issues": ["Lycopodium Clavatum", "Phosphorus", "Calcarea Carbonica"],
    "Sneezing": ["Natrum Muriaticum", "Arsenicum Album", "Pulsatilla Nigricans"],
    "Shortness of breath": ["Arsenicum Album", "Phosphorus", "Pulsatilla Nigricans"],
    "Wheezing": ["Arsenicum Album", "Phosphorus", "Pulsatilla Nigricans"],
    "Vomiting": ["Arsenicum Album", "Nux Vomica", "Ignatia Amara"],
    "Loss of appetite": ["Nux Vomica", "Ignatia Amara", "Sepia Officinalis"],
    "Food intolerance": ["Nux Vomica", "Lycopodium Clavatum", "Pulsatilla Nigricans"],
    "Heartburn": ["Nux Vomica", "Arsenicum Album", "Phosphorus"],
    "Flatulence": ["Lycopodium Clavatum", "Nux Vomica", "Sulphur"],
    "Neck pain": ["Rhus Toxicodendron", "Bryonia Alba", "Calcarea Carbonica"],
    "Rheumatism": ["Rhus Toxicodendron", "Bryonia Alba", "Sulphur"],
    "Warts": ["Calcarea Carbonica", "Lycopodium Clavatum", "Sulphur"],
    "Fungal infection": ["Sulphur", "Arsenicum Album", "Sepia Officinalis"],
    "Dry skin": ["Arsenicum Album", "Sulphur", "Natrum Muriaticum"],
    "Boils": ["Sulphur", "Belladonna", "Arsenicum Album"],
    "Weight loss": ["Arsenicum Album", "Phosphorus", "Natrum Muriaticum"],
    "Swelling": ["Bryonia Alba", "Rhus Toxicodendron", "Pulsatilla Nigricans"],
    "Numbness": ["Phosphorus", "Rhus Toxicodendron", "Calcarea Carbonica"],
    "Cold extremities": ["Arsenicum Album", "Calcarea Carbonica", "Phosphorus"],
}

# Initialize OpenAI client
def init_openai():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        try:
            api_key = st.secrets['openai']['api_key']
        except Exception:
            pass
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            return client
        except Exception:
            pass
    return None

# Initialize session state
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'constitution_result' not in st.session_state:
    st.session_state.constitution_result = None
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []
if 'diagnosis_result' not in st.session_state:
    st.session_state.diagnosis_result = None
if 'prescription_result' not in st.session_state:
    st.session_state.prescription_result = None

PATIENT_CONTEXT = {
    "name": "Ravi Sharma",
    "role": "patient",
    "age": 42,
    "gender": "Male",
    "chief_complaint": "Chronic digestive issues",
    "location": "New Delhi, India"
}

PRACTITIONER_CONTEXT = {
    "name": "Dr. Meera Joshi",
    "role": "practitioner",
    "department": "Homeopathic Medicine",
    "experience": "12 years",
    "specializations": ["Constitutional Prescribing", "Chronic Disease Management", "Pediatric Homeopathy"]
}


def generate_ai_response(message, user_context, provider="openai"):
    client = init_openai()
    if client:
        try:
            system_prompt = f"""You are NaturoSage, an AI-powered Homeopathy Assistant. You are knowledgeable in classical homeopathy, materia medica, repertory, and the principles of similimum.

User Context:
- Name: {user_context['name']}
- Role: {user_context['role']}
- Current Date: {datetime.now().strftime('%B %d, %Y')}

Your role is to:
1. Help users understand their homeopathic constitution
2. Assist with symptom analysis using homeopathic repertory principles
3. Suggest possible homeopathic remedies based on symptom totality
4. Explain remedy pictures, modalities, and potency guidelines
5. Educate about homeopathic principles (Law of Similars, Minimum Dose, Single Remedy)
6. Always recommend consulting a qualified homeopathic practitioner for actual treatment

Important guidelines:
- Always emphasize that AI suggestions are educational and not a substitute for professional consultation
- Use proper homeopathic terminology (modalities, miasms, potency, etc.)
- Consider the totality of symptoms, not just individual symptoms
- Be warm, empathetic, and supportive
- Explain concepts in simple language when speaking to patients"""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.warning(f"OpenAI API error: {e}. Using demo mode.")
            return generate_demo_response(message, user_context)
    return generate_demo_response(message, user_context)


def generate_demo_response(message, user_context):
    user_name = user_context['name'].split(' ')[0]
    lower_message = message.lower().strip()

    if 'constitution' in lower_message:
        return f"Great question, {user_name}! In homeopathy, your constitution is your unique physical, mental, and emotional makeup. It helps determine your constitutional remedy — the remedy that matches your overall pattern, not just individual symptoms. Use the Constitution Detector in the sidebar to discover yours!"

    if 'potency' in lower_message or 'dose' in lower_message:
        return f"{user_name}, potency selection is crucial in homeopathy. Lower potencies (6C, 12C) are used for acute physical conditions, 30C for general acute/chronic use, and higher potencies (200C, 1M) for deep constitutional treatment. Always start lower and move higher based on response. A qualified practitioner can guide you on the right potency."

    if 'arnica' in lower_message:
        return f"Arnica Montana is one of the most popular homeopathic remedies! It's the go-to for physical trauma, bruising, muscle soreness, and post-surgical recovery. Key symptom: the patient says 'I'm fine' even when clearly not. Use 30C for acute injuries, repeat as needed. It's also great for overexertion."

    if any(word in lower_message for word in ['anxiety', 'anxious', 'worry', 'fear']):
        return f"{user_name}, several homeopathic remedies address anxiety. Aconitum for sudden panic/fear, Arsenicum Album for restless anxiety worse at midnight, Phosphorus for anxiety about health with desire for company, and Calcarea Carbonica for worry about security. The specific remedy depends on your unique symptom picture and constitution."

    if any(word in lower_message for word in ['skin', 'eczema', 'rash', 'itch']):
        return f"Skin conditions respond well to homeopathy, {user_name}. Key remedies include Sulphur (burning, itching worse from heat/bathing), Arsenicum Album (dry, scaly, burning better from warmth), Graphites (oozing, sticky discharges), and Natrum Muriaticum (dry eczema at hairline). Constitutional treatment often gives the best long-term results for chronic skin issues."

    if any(word in lower_message for word in ['digest', 'stomach', 'bloat', 'acid', 'gas']):
        return f"Digestive complaints are very common in homeopathic practice, {user_name}. Top remedies include Nux Vomica (overindulgence, irritability), Lycopodium (bloating 4-8 PM, right-sided), Pulsatilla (worse from rich/fatty food), and Arsenicum (burning pains, food poisoning). Try our Symptom Checker to get a personalized analysis!"

    if any(word in lower_message for word in ['hello', 'hi', 'hey']):
        return f"Hello {user_name}! 🌿 I'm NaturoSage, your Homeopathy Assistant. I can help you understand homeopathic constitutions, check symptoms, explore remedies, and learn about this gentle healing system. What would you like to explore today?"

    if 'thank' in lower_message:
        return f"You're welcome, {user_name}! Remember, homeopathy treats the whole person, not just the disease. Feel free to explore the Constitution Detector, Symptom Checker, or ask me anything about homeopathic remedies. 🌿"

    if any(word in lower_message for word in ['what is homeopathy', 'homeopathy']):
        return f"Homeopathy is a natural system of medicine founded by Dr. Samuel Hahnemann in the late 18th century. It's based on the principle 'Similia Similibus Curentur' — Like Cures Like. A substance that causes symptoms in a healthy person can cure similar symptoms in a sick person when given in highly diluted form. It's gentle, non-toxic, and treats the whole person — mind, body, and emotions."

    if any(c in lower_message for c in ['?', 'what', 'how', 'why', 'when', 'which']):
        return f"That's a thoughtful question, {user_name}. I can help with information about homeopathic remedies, constitutions, symptom analysis, potency selection, and general homeopathic principles. Could you share more details so I can give you the most relevant guidance?"

    return f"I understand you're asking about \"{message}\", {user_name}. I'm NaturoSage, your Homeopathy Assistant. I can help with constitution analysis, symptom checking, remedy suggestions, and homeopathic education. Try using our specialized tools in the menu, or ask me a specific question about homeopathy!"


def determine_constitution(answers):
    scores = {name: 0 for name in CONSTITUTIONS}

    body_map = {
        "Stocky / tendency to gain weight": ["Calcarea Carbonica"],
        "Tall and slender": ["Phosphorus"],
        "Lean / wiry / tense": ["Nux Vomica", "Arsenicum Album"],
        "Soft / plump": ["Pulsatilla"],
        "Average build": ["Lycopodium", "Sulphur", "Natrum Muriaticum"]
    }
    for const in body_map.get(answers.get("body_type", ""), []):
        scores[const] = scores.get(const, 0) + 2

    temp_map = {
        "Very chilly — hate cold weather": ["Calcarea Carbonica", "Arsenicum Album", "Nux Vomica"],
        "Warm-blooded — dislike heat": ["Sulphur", "Pulsatilla"],
        "Mixed — affected by both extremes": ["Phosphorus", "Natrum Muriaticum", "Lycopodium"]
    }
    for const in temp_map.get(answers.get("thermal", ""), []):
        scores[const] = scores.get(const, 0) + 2

    food_map = {
        "Eggs, dairy, starchy food": ["Calcarea Carbonica"],
        "Cold drinks, ice cream, salt": ["Phosphorus"],
        "Spicy food, stimulants, alcohol": ["Nux Vomica", "Sulphur"],
        "Rich food, butter, cream": ["Pulsatilla"],
        "Salt and sour foods": ["Natrum Muriaticum"],
        "Warm drinks, sweets": ["Lycopodium", "Arsenicum Album"]
    }
    for const in food_map.get(answers.get("food_craving", ""), []):
        scores[const] = scores.get(const, 0) + 2

    temperament_map = {
        "Cautious, anxious, methodical": ["Calcarea Carbonica"],
        "Open, sociable, sympathetic": ["Phosphorus"],
        "Intellectual, philosophical, untidy": ["Sulphur"],
        "Driven, competitive, irritable": ["Nux Vomica"],
        "Reserved, serious, holds grudges": ["Natrum Muriaticum"],
        "Gentle, weepy, changeable moods": ["Pulsatilla"],
        "Anxious, restless, perfectionist": ["Arsenicum Album"],
        "Intellectual but insecure": ["Lycopodium"]
    }
    for const in temperament_map.get(answers.get("temperament", ""), []):
        scores[const] = scores.get(const, 0) + 3

    sleep_map = {
        "Sweats on head/neck at night": ["Calcarea Carbonica"],
        "Restless after midnight (12-2 AM)": ["Arsenicum Album"],
        "Can't sleep from mental overwork": ["Nux Vomica"],
        "Sleeps on back with arms above head": ["Pulsatilla"],
        "Light sleeper, sensitive to noise": ["Phosphorus"],
        "Feels unrested, worse in morning": ["Sulphur", "Lycopodium", "Natrum Muriaticum"]
    }
    for const in sleep_map.get(answers.get("sleep", ""), []):
        scores[const] = scores.get(const, 0) + 2

    emotion_map = {
        "Fear of illness and health anxiety": ["Calcarea Carbonica", "Arsenicum Album"],
        "Fear of being alone, craves company": ["Phosphorus"],
        "Fear of public speaking / stage fright": ["Lycopodium"],
        "Grief held inside, avoids consolation": ["Natrum Muriaticum"],
        "Weeps easily, wants comfort": ["Pulsatilla"],
        "Irritable, critical, impatient": ["Nux Vomica"],
        "Burning concerns, restless worrying": ["Arsenicum Album"]
    }
    for const in emotion_map.get(answers.get("emotions", ""), []):
        scores[const] = scores.get(const, 0) + 3

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top = sorted_scores[0]
    runner_up = sorted_scores[1] if len(sorted_scores) > 1 else None

    return top, runner_up, sorted_scores


def get_remedies_for_symptoms(selected_symptoms, modality_worse="", modality_better=""):
    remedy_scores = {}
    for symptom in selected_symptoms:
        remedies = SYMPTOM_TO_REMEDIES.get(symptom, [])
        for remedy in remedies:
            remedy_scores[remedy] = remedy_scores.get(remedy, 0) + 1

    sorted_remedies = sorted(remedy_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_remedies[:5]


# ============ MAIN APP ============

def main():
    st.markdown("""
    <div class="main-header">
        <h1>🌿 NaturoSage</h1>
        <p>AI-Powered Homeopathy Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.user_role is None:
        st.markdown("### 👋 Welcome! Choose your role to get started:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧑 Login as Patient (Ravi Sharma)", use_container_width=True):
                st.session_state.user_role = "patient"
                st.session_state.user_name = PATIENT_CONTEXT["name"]
                st.session_state.chat_history = []
                st.rerun()
        with col2:
            if st.button("👩‍⚕️ Login as Practitioner (Dr. Meera Joshi)", use_container_width=True):
                st.session_state.user_role = "practitioner"
                st.session_state.user_name = PRACTITIONER_CONTEXT["name"]
                st.session_state.chat_history = []
                st.rerun()
    else:
        user_context = PATIENT_CONTEXT if st.session_state.user_role == "patient" else PRACTITIONER_CONTEXT

        with st.sidebar:
            card_class = 'user-card' if st.session_state.user_role == 'patient' else 'practitioner-card'
            html_content = f'<div class="{card_class}"><h3>🌿 Welcome, {st.session_state.user_name}!</h3>'
            html_content += f'<p><strong>Role:</strong> {st.session_state.user_role.title()}</p>'
            if st.session_state.user_role == "patient":
                html_content += f'<p><strong>Age:</strong> {user_context["age"]} • <strong>Gender:</strong> {user_context["gender"]}</p>'
            else:
                html_content += f'<p><strong>Dept:</strong> {user_context["department"]}</p>'
            html_content += "</div>"
            st.markdown(html_content, unsafe_allow_html=True)

            st.markdown("### 📋 Navigation")
            page = st.radio("Go to:", [
                "🏠 Dashboard",
                "🧬 Constitution Detector",
                "🔍 Symptom Checker",
                "📋 Diagnosis",
                "💊 Prescription",
                "🤖 AI Chat",
                "📚 Materia Medica"
            ], label_visibility="collapsed")

            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user_role = None
                st.session_state.user_name = None
                st.session_state.chat_history = []
                st.session_state.constitution_result = None
                st.session_state.selected_symptoms = []
                st.session_state.diagnosis_result = None
                st.session_state.prescription_result = None
                st.rerun()

        if page == "🏠 Dashboard":
            show_dashboard(user_context)
        elif page == "🧬 Constitution Detector":
            show_constitution_detector(user_context)
        elif page == "🔍 Symptom Checker":
            show_symptom_checker(user_context)
        elif page == "📋 Diagnosis":
            show_diagnosis(user_context)
        elif page == "💊 Prescription":
            show_prescription(user_context)
        elif page == "🤖 AI Chat":
            show_ai_chat(user_context)
        elif page == "📚 Materia Medica":
            show_materia_medica()


def show_dashboard(user_context):
    if st.session_state.user_role == "patient":
        st.markdown(f"""
        <div class="user-card">
            <h2>Welcome back, {user_context['name'].split(' ')[0]}! 🌿</h2>
            <p>Your holistic health journey starts here.</p>
            <p><strong>Age:</strong> {user_context['age']} • <strong>Chief Complaint:</strong> {user_context['chief_complaint']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🗺️ Your Healing Journey")
        j1, j2, j3, j4 = st.columns(4)
        with j1:
            st.markdown("""<div class="constitution-card"><h5>🧬 Step 1</h5><p style="margin:0">Constitution<br>Detection</p></div>""", unsafe_allow_html=True)
        with j2:
            st.markdown("""<div class="constitution-card"><h5>🔍 Step 2</h5><p style="margin:0">Symptom<br>Check</p></div>""", unsafe_allow_html=True)
        with j3:
            st.markdown("""<div class="constitution-card"><h5>📋 Step 3</h5><p style="margin:0">Diagnosis<br>Analysis</p></div>""", unsafe_allow_html=True)
        with j4:
            st.markdown("""<div class="constitution-card"><h5>💊 Step 4</h5><p style="margin:0">Remedy<br>Prescription</p></div>""", unsafe_allow_html=True)

        st.markdown("### 📊 Quick Stats")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            const_status = "✅ Done" if st.session_state.constitution_result else "⏳ Pending"
            st.markdown(f'<div class="metric-card"><h3 style="font-size:1.2rem;">🧬</h3><p>Constitution: {const_status}</p></div>', unsafe_allow_html=True)
        with c2:
            symp_count = len(st.session_state.selected_symptoms)
            st.markdown(f'<div class="metric-card"><h3 style="font-size:1.2rem;">🔍</h3><p>Symptoms: {symp_count} logged</p></div>', unsafe_allow_html=True)
        with c3:
            diag_status = "✅ Done" if st.session_state.diagnosis_result else "⏳ Pending"
            st.markdown(f'<div class="metric-card"><h3 style="font-size:1.2rem;">📋</h3><p>Diagnosis: {diag_status}</p></div>', unsafe_allow_html=True)
        with c4:
            rx_status = "✅ Done" if st.session_state.prescription_result else "⏳ Pending"
            st.markdown(f'<div class="metric-card"><h3 style="font-size:1.2rem;">💊</h3><p>Prescription: {rx_status}</p></div>', unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="practitioner-card">
            <h2>Welcome, {user_context['name']}! 👩‍⚕️</h2>
            <p><strong>Department:</strong> {user_context['department']} • <strong>Experience:</strong> {user_context['experience']}</p>
            <p>Specializations: {', '.join(user_context['specializations'])}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Practice Overview")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<div class="metric-card"><h3>24</h3><p>Active Patients</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card"><h3>156</h3><p>Remedies Prescribed</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-card"><h3>89%</h3><p>Recovery Rate</p></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="metric-card"><h3>4.8⭐</h3><p>Patient Rating</p></div>', unsafe_allow_html=True)

        st.markdown("### 👥 Recent Patients")
        patients = [
            {"name": "Ravi Sharma", "complaint": "Chronic digestive issues", "constitution": "Lycopodium", "status": "Follow-up"},
            {"name": "Priya Patel", "complaint": "Recurrent migraines", "constitution": "Natrum Mur", "status": "New"},
            {"name": "Amit Kumar", "complaint": "Skin eczema", "constitution": "Sulphur", "status": "Improving"},
        ]
        for p in patients:
            with st.expander(f"👤 {p['name']} — {p['status']}"):
                st.write(f"**Chief Complaint:** {p['complaint']}")
                st.write(f"**Constitution:** {p['constitution']}")
                st.write(f"**Status:** {p['status']}")


def show_constitution_detector(user_context):
    st.markdown("### 🧬 Constitution Detector")
    st.markdown("Answer these questions to discover your homeopathic constitution (body-mind type). This helps identify your **constitutional remedy**.")

    with st.form("constitution_form"):
        body_type = st.selectbox("1. What best describes your body type?", [
            "Select...", "Stocky / tendency to gain weight", "Tall and slender",
            "Lean / wiry / tense", "Soft / plump", "Average build"
        ])
        thermal = st.selectbox("2. How do you respond to temperature?", [
            "Select...", "Very chilly — hate cold weather",
            "Warm-blooded — dislike heat", "Mixed — affected by both extremes"
        ])
        food_craving = st.selectbox("3. What foods do you crave most?", [
            "Select...", "Eggs, dairy, starchy food", "Cold drinks, ice cream, salt",
            "Spicy food, stimulants, alcohol", "Rich food, butter, cream",
            "Salt and sour foods", "Warm drinks, sweets"
        ])
        temperament = st.selectbox("4. Which temperament fits you best?", [
            "Select...", "Cautious, anxious, methodical", "Open, sociable, sympathetic",
            "Intellectual, philosophical, untidy", "Driven, competitive, irritable",
            "Reserved, serious, holds grudges", "Gentle, weepy, changeable moods",
            "Anxious, restless, perfectionist", "Intellectual but insecure"
        ])
        sleep = st.selectbox("5. What is your sleep pattern like?", [
            "Select...", "Sweats on head/neck at night",
            "Restless after midnight (12-2 AM)", "Can't sleep from mental overwork",
            "Sleeps on back with arms above head", "Light sleeper, sensitive to noise",
            "Feels unrested, worse in morning"
        ])
        emotions = st.selectbox("6. Which emotional pattern resonates with you?", [
            "Select...", "Fear of illness and health anxiety",
            "Fear of being alone, craves company", "Fear of public speaking / stage fright",
            "Grief held inside, avoids consolation", "Weeps easily, wants comfort",
            "Irritable, critical, impatient", "Burning concerns, restless worrying"
        ])

        submitted = st.form_submit_button("🧬 Detect My Constitution", use_container_width=True)

        if submitted:
            if any(v == "Select..." for v in [body_type, thermal, food_craving, temperament, sleep, emotions]):
                st.error("Please answer all questions to get an accurate result.")
            else:
                answers = {
                    "body_type": body_type, "thermal": thermal, "food_craving": food_craving,
                    "temperament": temperament, "sleep": sleep, "emotions": emotions
                }
                top, runner_up, all_scores = determine_constitution(answers)
                st.session_state.constitution_result = {"top": top, "runner_up": runner_up, "all_scores": all_scores}
                st.rerun()

    if st.session_state.constitution_result:
        result = st.session_state.constitution_result
        top_name, top_score = result["top"]
        const_info = CONSTITUTIONS.get(top_name, {})

        st.markdown("---")
        st.markdown(f"### 🎯 Your Primary Constitution: **{top_name}**")
        st.markdown(f"""
        <div class="remedy-card">
            <h4 style="color: #2e7d32; margin-bottom: 0.5rem;">{top_name} Constitution</h4>
            <p><strong>Body Type:</strong> {const_info.get('body_type', 'N/A')}</p>
            <p><strong>Temperament:</strong> {const_info.get('temperament', 'N/A')}</p>
            <p><strong>Thermal:</strong> {const_info.get('thermal', 'N/A')}</p>
            <p><strong>Food Cravings:</strong> {const_info.get('food_cravings', 'N/A')}</p>
            <p><strong>Food Aversions:</strong> {const_info.get('food_aversions', 'N/A')}</p>
            <p><strong>Key Features:</strong></p>
            <ul>{''.join(f'<li>{f}</li>' for f in const_info.get('key_features', []))}</ul>
        </div>
        """, unsafe_allow_html=True)

        if result["runner_up"]:
            ru_name, ru_score = result["runner_up"]
            st.info(f"🔄 Runner-up constitution: **{ru_name}** (score: {ru_score})")

        st.caption("⚠️ This is an educational tool. Please consult a qualified homeopathic practitioner for accurate constitutional prescribing.")


def show_symptom_checker(user_context):
    st.markdown("### 🔍 Symptom Checker")
    st.markdown("Select your symptoms across different body systems. The more specific you are, the better the analysis.")

    selected = []
    for category, symptoms in SYMPTOM_CATEGORIES.items():
        with st.expander(f"📂 {category}"):
            chosen = st.multiselect(f"Select symptoms in {category}:", symptoms, key=f"sym_{category}")
            selected.extend(chosen)

    st.markdown("---")
    st.markdown("### ⏰ Modalities (What makes symptoms better or worse?)")
    col1, col2 = st.columns(2)
    with col1:
        worse = st.multiselect("Worse from:", [
            "Morning", "Evening", "Night", "Cold", "Heat", "Motion", "Rest",
            "Touch", "Eating", "After sleep", "Dampness", "Before storms"
        ])
    with col2:
        better = st.multiselect("Better from:", [
            "Warmth", "Cold applications", "Rest", "Motion", "Open air",
            "Pressure", "Eating", "Company", "Alone", "After sleep"
        ])

    if st.button("🔍 Analyze Symptoms", use_container_width=True):
        if not selected:
            st.error("Please select at least one symptom.")
        else:
            st.session_state.selected_symptoms = selected
            st.session_state.symptom_modalities = {"worse": worse, "better": better}
            st.success(f"✅ {len(selected)} symptom(s) recorded! Go to **Diagnosis** for analysis.")

    if st.session_state.selected_symptoms:
        st.markdown("### 📋 Your Current Symptoms")
        symptom_html = " ".join(f'<span class="symptom-tag">{s}</span>' for s in st.session_state.selected_symptoms)
        st.markdown(symptom_html, unsafe_allow_html=True)


def show_diagnosis(user_context):
    st.markdown("### 📋 Homeopathic Diagnosis")

    if not st.session_state.selected_symptoms:
        st.warning("⚠️ No symptoms recorded yet. Please use the **Symptom Checker** first.")
        return

    st.markdown("#### Current Symptoms")
    symptom_html = " ".join(f'<span class="symptom-tag">{s}</span>' for s in st.session_state.selected_symptoms)
    st.markdown(symptom_html, unsafe_allow_html=True)

    if st.button("📋 Generate Diagnosis", use_container_width=True):
        remedies = get_remedies_for_symptoms(st.session_state.selected_symptoms)

        if not remedies:
            st.error("Could not determine matching remedies. Please add more symptoms.")
            return

        diagnosis_data = []
        for remedy_name, score in remedies:
            remedy_info = HOMEO_MATERIA_MEDICA.get(remedy_name, {})
            diagnosis_data.append({
                "name": remedy_name,
                "score": score,
                "common_name": remedy_info.get("common_name", ""),
                "indications": remedy_info.get("indications", ""),
                "key_symptoms": remedy_info.get("key_symptoms", [])
            })

        st.session_state.diagnosis_result = diagnosis_data
        st.rerun()

    if st.session_state.diagnosis_result:
        st.markdown("---")
        st.markdown("### 🎯 Diagnosis Results — Top Matching Remedies")

        for i, remedy in enumerate(st.session_state.diagnosis_result):
            match_pct = min(100, int((remedy["score"] / max(1, len(st.session_state.selected_symptoms))) * 100))
            st.markdown(f"""
            <div class="diagnosis-box">
                <h4 style="color: #e65100; margin-bottom: 0.5rem;">{'🥇' if i == 0 else '🥈' if i == 1 else '🥉' if i == 2 else '📌'} {remedy['name']} ({remedy['common_name']})</h4>
                <p><strong>Match Score:</strong> {remedy['score']} symptoms covered ({match_pct}% match)</p>
                <p><strong>Key Symptoms:</strong> {', '.join(remedy['key_symptoms'])}</p>
                <p><strong>Indications:</strong> {remedy['indications']}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.constitution_result:
            top_const = st.session_state.constitution_result["top"][0]
            st.info(f"🧬 Your constitution ({top_const}) has been considered in the analysis. Constitutional remedies often provide deeper, longer-lasting healing.")

        st.caption("⚠️ This analysis is educational. Always consult a qualified homeopathic practitioner for personalized treatment.")


def show_prescription(user_context):
    st.markdown("### 💊 Homeopathic Prescription")

    if not st.session_state.diagnosis_result:
        st.warning("⚠️ Please complete the **Diagnosis** step first.")
        return

    top_remedy_data = st.session_state.diagnosis_result[0]
    top_remedy_name = top_remedy_data["name"]
    remedy_info = HOMEO_MATERIA_MEDICA.get(top_remedy_name, {})

    st.markdown(f"""
    <div class="remedy-card">
        <h3 style="color: #2e7d32;">💊 Primary Remedy: {top_remedy_name}</h3>
        <p><strong>Common Name:</strong> {remedy_info.get('common_name', 'N/A')}</p>
        <p><strong>Recommended Potency:</strong> {remedy_info.get('potency', '30C')}</p>
        <p><strong>Indications:</strong> {remedy_info.get('indications', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📝 Prescription Details")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Remedy:** {top_remedy_name}")
        st.markdown(f"**Potency:** {remedy_info.get('potency', '30C')}")
        st.markdown(f"**Form:** Globules / Pills")
    with col2:
        modalities = remedy_info.get("modalities", {})
        st.markdown(f"**Worse from:** {modalities.get('worse', 'N/A')}")
        st.markdown(f"**Better from:** {modalities.get('better', 'N/A')}")

    st.markdown("#### 📋 Dosage Guidelines")
    st.markdown("""
    | Condition Type | Potency | Frequency | Duration |
    |---|---|---|---|
    | Acute (sudden onset) | 30C | Every 2-4 hours | Until improvement |
    | Subacute | 30C | 2-3 times daily | 1-2 weeks |
    | Chronic | 200C | Once weekly | 4-6 weeks |
    | Constitutional | 200C / 1M | Single dose | Wait & watch |
    """)

    st.markdown("#### 🔄 Alternative Remedies")
    for remedy in st.session_state.diagnosis_result[1:3]:
        alt_info = HOMEO_MATERIA_MEDICA.get(remedy["name"], {})
        st.markdown(f"""
        <div style="background: #f5f5f5; padding: 0.75rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #9e9e9e;">
            <strong>{remedy['name']}</strong> ({alt_info.get('common_name', '')}) — Potency: {alt_info.get('potency', '30C')}<br>
            <small>{alt_info.get('indications', '')}</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### ⚠️ Important Guidelines")
    st.warning("""
    **Homeopathic Prescription Guidelines:**
    - Take remedies 15-30 minutes away from food, drink, or strong flavors (mint, coffee)
    - Avoid touching pills with hands — tip into cap and place under tongue
    - Stop the remedy once significant improvement begins
    - If symptoms worsen briefly then improve, this is a good sign (homeopathic aggravation)
    - Consult your practitioner if no improvement after the recommended duration
    """)

    if st.button("💾 Save Prescription", use_container_width=True):
        st.session_state.prescription_result = {
            "remedy": top_remedy_name,
            "potency": remedy_info.get("potency", "30C"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "symptoms": st.session_state.selected_symptoms,
            "constitution": st.session_state.constitution_result["top"][0] if st.session_state.constitution_result else "Not assessed"
        }
        st.success("✅ Prescription saved! You can view it from your Dashboard.")

    st.caption("⚠️ This prescription is for educational purposes only. Always follow guidance from a qualified homeopathic practitioner.")


def show_ai_chat(user_context):
    st.markdown("### 🤖 NaturoSage AI Chat")
    st.markdown("Ask me anything about homeopathy, remedies, constitutions, or your health concerns.")

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message ai-message"><strong>🌿 NaturoSage:</strong> {message["content"]}</div>', unsafe_allow_html=True)

    user_input = st.text_input("Ask about homeopathy, remedies, or your symptoms:", placeholder="e.g., What remedy is good for anxiety?")

    if st.button("🌿 Ask NaturoSage", use_container_width=True):
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
            with st.spinner("NaturoSage is thinking..."):
                ai_response = generate_ai_response(user_input, user_context)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response, "timestamp": datetime.now()})
            st.rerun()

    st.markdown("#### 💡 Quick Questions")
    quick_qs = [
        "What is homeopathy?",
        "Tell me about Arnica",
        "How to choose potency?",
        "Remedies for anxiety?"
    ]
    qcols = st.columns(len(quick_qs))
    for i, q in enumerate(quick_qs):
        with qcols[i]:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": q, "timestamp": datetime.now()})
                with st.spinner("NaturoSage is thinking..."):
                    response = generate_ai_response(q, user_context)
                st.session_state.chat_history.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                st.rerun()


def show_materia_medica():
    st.markdown("### 📚 Homeopathic Materia Medica")
    st.markdown("Browse the key remedies in our database.")

    search = st.text_input("🔎 Search remedies:", placeholder="e.g., Arnica, Belladonna...")

    for name, info in HOMEO_MATERIA_MEDICA.items():
        if search and search.lower() not in name.lower() and search.lower() not in info.get("common_name", "").lower():
            continue
        with st.expander(f"💊 {name} ({info.get('common_name', '')})"):
            st.markdown(f"**Key Symptoms:** {', '.join(info.get('key_symptoms', []))}")
            modalities = info.get("modalities", {})
            st.markdown(f"**Worse from:** {modalities.get('worse', 'N/A')}")
            st.markdown(f"**Better from:** {modalities.get('better', 'N/A')}")
            st.markdown(f"**Recommended Potency:** {info.get('potency', '30C')}")
            st.markdown(f"**Indications:** {info.get('indications', 'N/A')}")


if __name__ == "__main__":
    main()
