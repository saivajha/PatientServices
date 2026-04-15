# 🌿 NaturoSage - AI-Powered Homeopathy Assistant

A comprehensive AI-powered homeopathy platform featuring constitution detection, symptom checking, diagnosis analysis, and homeopathic medicine prescription.

## Features

### 🧬 Constitution Detector
- Questionnaire-based homeopathic constitution assessment
- Identifies primary and secondary constitutional types
- Covers 8 major constitutions: Calcarea Carb, Phosphorus, Sulphur, Lycopodium, Natrum Mur, Pulsatilla, Nux Vomica, Arsenicum Album

### 🔍 Symptom Checker
- Multi-system symptom selection (Head & Mind, Respiratory, Digestive, Musculoskeletal, Skin, General)
- Modality tracking (what makes symptoms better/worse)
- Symptom totality analysis

### 📋 Diagnosis
- Repertory-based remedy matching using symptom totality
- Ranked remedy suggestions with match scores
- Constitutional correlation

### 💊 Prescription
- Detailed remedy information with potency guidelines
- Dosage schedules for acute, subacute, and chronic conditions
- Alternative remedy suggestions
- Important homeopathic guidelines

### 🤖 AI Chat (NaturoSage AI)
- OpenAI GPT-4 powered conversational assistant
- Homeopathic knowledge base with demo fallback mode
- Quick question shortcuts

### 📚 Materia Medica
- Searchable database of 15+ key homeopathic remedies
- Key symptoms, modalities, potency, and indications

## Quick Start

### Streamlit App (Primary)
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Open http://localhost:8501

### Express.js Server (Secondary)
```bash
npm install
npm run dev
```
Open http://localhost:3000

## Configuration

### Optional: OpenAI API Key
Set `OPENAI_API_KEY` as an environment variable for real AI responses. Without it, the app works fully in demo mode with built-in homeopathic knowledge.

## User Roles

### Patient (Ravi Sharma)
- Run through the healing journey: Constitution → Symptoms → Diagnosis → Prescription
- Chat with NaturoSage AI about homeopathy
- Browse Materia Medica

### Practitioner (Dr. Meera Joshi)
- View patient records and consultation history
- Test AI configurations across providers
- Monitor practice metrics

## Tech Stack

- **Frontend (Primary)**: Streamlit (Python)
- **Frontend (Secondary)**: Express.js + Tailwind CSS
- **AI**: OpenAI GPT-4 (with demo fallback)
- **Deployment**: Streamlit Cloud / Heroku

## Disclaimer

NaturoSage is an educational tool. Always consult a qualified homeopathic practitioner for actual treatment decisions.

---

**Built with 🌿 by the NaturoSage Team**
