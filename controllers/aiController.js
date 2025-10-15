const OpenAI = require('openai');
const axios = require('axios');

// Initialize OpenAI client
const openai = process.env.OPENAI_API_KEY ? new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
}) : null;

class AIController {
  
  // Generate AI response
  async generateResponse(req, res) {
    try {
      const { message, provider = 'openai', context = {} } = req.body;
      const user = req.user;

      if (!message || message.trim().length === 0) {
        return res.status(400).json({ error: 'Message is required' });
      }

      let response;
      
      switch (provider) {
        case 'openai':
          response = await this.callOpenAI(message, user, context);
          break;
        case 'gemini':
          response = await this.callGemini(message, user, context);
          break;
        case 'claude':
          response = await this.callClaude(message, user, context);
          break;
        case 'demo':
        default:
          response = this.generateDemoResponse(message, user);
          break;
      }

      res.json({ 
        response,
        provider,
        timestamp: new Date().toISOString(),
        user: user.name
      });

    } catch (error) {
      console.error('AI Controller Error:', error);
      res.status(500).json({ 
        error: 'Failed to generate AI response',
        message: error.message,
        fallback: this.generateDemoResponse(req.body.message, req.user)
      });
    }
  }

  // OpenAI API call
  async callOpenAI(message, user, context) {
    if (!openai) {
      throw new Error('OpenAI API key not configured');
    }

    const systemPrompt = this.createSystemPrompt(user, context);
    
    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: message }
      ],
      max_tokens: 300,
      temperature: 0.7,
      presence_penalty: 0.1,
      frequency_penalty: 0.1
    });

    return completion.choices[0].message.content.trim();
  }

  // Google Gemini API call
  async callGemini(message, user, context) {
    if (!process.env.GOOGLE_API_KEY) {
      throw new Error('Google API key not configured');
    }

    const systemPrompt = this.createSystemPrompt(user, context);
    
    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${process.env.GOOGLE_API_KEY}`,
      {
        contents: [{
          parts: [{
            text: `${systemPrompt}\n\nPatient question: ${message}`
          }]
        }]
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data.candidates[0].content.parts[0].text;
  }

  // Anthropic Claude API call
  async callClaude(message, user, context) {
    if (!process.env.ANTHROPIC_API_KEY) {
      throw new Error('Anthropic API key not configured');
    }

    const systemPrompt = this.createSystemPrompt(user, context);
    
    const response = await axios.post(
      'https://api.anthropic.com/v1/messages',
      {
        model: 'claude-3-sonnet-20240229',
        max_tokens: 300,
        messages: [
          { role: 'user', content: `${systemPrompt}\n\nPatient question: ${message}` }
        ]
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': process.env.ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01'
        }
      }
    );

    return response.data.content[0].text;
  }

  // Create system prompt for LLM
  createSystemPrompt(user, context) {
    return `You are an AI assistant for Biogen Patient Services, specifically helping patients with Multiple Sclerosis (MS) who are on Tysabri therapy. You are empathetic, knowledgeable, and supportive.

Patient Context:
- Name: ${user.name}
- Role: ${user.role}
- Diagnosis: ${context.diagnosis || "Relapsing-Remitting MS"}
- Therapy: ${context.therapy || "Tysabri"}
- Diagnosis Date: ${context.diagnosisDate || "October 20, 2025"}
- Next Infusion: ${context.nextInfusion || "October 25, 2025"}
- Location: ${context.location || "Palo Alto, CA"}
- Current Date: ${new Date().toLocaleDateString()}

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
- If you don't know something, admit it and suggest who might know`;
  }

  // Enhanced demo mode responses
  generateDemoResponse(message, user) {
    const userName = user.name.split(' ')[0];
    const lowerMessage = message.toLowerCase().trim();
    
    // Personal questions
    if (lowerMessage.includes('what is my name') || lowerMessage.includes('my name')) {
      return `Your name is ${user.name}. I'm here to help you with your Tysabri treatment journey.`;
    }
    
    if (lowerMessage.includes('who am i') || lowerMessage.includes('who are you talking to')) {
      return `I'm talking to ${user.name}. You're a patient starting Tysabri treatment for MS. How can I help you today?`;
    }
    
    // Medical questions
    if (lowerMessage.includes('what is tysabri') || lowerMessage.includes('tysabri')) {
      return `Tysabri (natalizumab) is a medication used to treat relapsing-remitting multiple sclerosis. It's given as an IV infusion every 28 days and helps reduce MS inflammation and relapses. You'll be starting this treatment on October 25, 2025. Do you have any specific questions about how it works?`;
    }
    
    if (lowerMessage.includes('side effects') || lowerMessage.includes('side effect')) {
      return `Common side effects of Tysabri can include headache, fatigue, nausea, and sometimes mild flu-like symptoms, especially in the first few infusions. Most people tolerate it well, and side effects usually improve over time. Your healthcare team will monitor you closely for any concerns. Are you worried about any particular side effects?`;
    }
    
    if (lowerMessage.includes('headache') || lowerMessage.includes('head pain')) {
      return `Headaches can happen with Tysabri, especially after infusions. You can usually take acetaminophen (Tylenol) for relief. Stay hydrated and rest in a cool, dark room if needed. Most infusion-related headaches improve within 24-48 hours. Is this something you're experiencing?`;
    }
    
    // Appointment questions
    if (lowerMessage.includes('when is my appointment') || lowerMessage.includes('when is my infusion') || lowerMessage.includes('appointment')) {
      return `Your next infusion is scheduled for October 25, 2025. After that, you'll have infusions every 28 days. I can help you schedule future appointments or reschedule if needed. Would you like me to help you with anything specific about your appointment?`;
    }
    
    // Transportation
    if (lowerMessage.includes('transportation') || lowerMessage.includes('ride') || lowerMessage.includes('uber') || lowerMessage.includes('how do i get there')) {
      return `I can help you arrange transportation to your appointments! We can coordinate Uber or Lyft rides, medical transportation, or help you coordinate with family or friends. Just let me know your address and I can set up a ride for your October 25th appointment. Would you like me to help arrange that now?`;
    }
    
    // Emotional support
    if (lowerMessage.includes('worried') || lowerMessage.includes('anxious') || lowerMessage.includes('scared') || lowerMessage.includes('nervous')) {
      return `It's completely normal to feel worried or anxious about starting a new treatment, especially with a new MS diagnosis. Many people feel this way. Tysabri is a very effective treatment, and your healthcare team will monitor you closely. You're taking the right steps by getting treatment early. Is there something specific that's worrying you? I'm here to listen and help.`;
    }
    
    // Greetings
    if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
      return `Hello ${userName}! I'm your AI assistant for your Tysabri treatment journey. I can help you with questions about MS, your treatment, appointments, side effects, or anything else you're curious about. What would you like to know?`;
    }
    
    if (lowerMessage.includes('thank you') || lowerMessage.includes('thanks')) {
      return `You're very welcome, ${userName}! I'm glad I could help. Is there anything else you'd like to know about your treatment or MS?`;
    }
    
    // General fallback
    if (lowerMessage.includes('?') || lowerMessage.includes('what') || lowerMessage.includes('how') || lowerMessage.includes('why') || lowerMessage.includes('when') || lowerMessage.includes('where')) {
      return `That's a great question, ${userName}. I want to make sure I give you the most accurate and helpful information. Could you provide a bit more detail about what specifically you'd like to know? I can help with questions about MS, Tysabri treatment, appointments, side effects, lifestyle, family, work, or any other concerns you might have.`;
    }
    
    // Final fallback
    return `I understand you're asking about "${message}", ${userName}. I'm your AI assistant for your Tysabri treatment journey. I can help you with questions about MS, your medication, appointments, side effects, lifestyle, family, work, or anything else on your mind. Could you tell me more about what you'd like to know? I'm here to support you.`;
  }

  // Get available providers
  async getProviders(req, res) {
    const providers = [
      { id: 'openai', name: 'OpenAI GPT-4', available: !!process.env.OPENAI_API_KEY },
      { id: 'gemini', name: 'Google Gemini Pro', available: !!process.env.GOOGLE_API_KEY },
      { id: 'claude', name: 'Anthropic Claude', available: !!process.env.ANTHROPIC_API_KEY },
      { id: 'demo', name: 'Demo Mode', available: true }
    ];

    res.json({ providers });
  }

  // Test AI connection
  async testConnection(req, res) {
    try {
      const { provider = 'openai' } = req.query;
      
      let response;
      switch (provider) {
        case 'openai':
          response = await this.callOpenAI('Hello, are you working?', req.user, {});
          break;
        case 'demo':
        default:
          response = this.generateDemoResponse('Hello, are you working?', req.user);
          break;
      }

      res.json({ 
        success: true, 
        provider,
        response,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      res.status(500).json({ 
        success: false, 
        error: error.message,
        provider: req.query.provider || 'openai'
      });
    }
  }
}

module.exports = new AIController();
