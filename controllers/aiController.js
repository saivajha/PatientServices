const OpenAI = require('openai');
const axios = require('axios');

const openai = process.env.OPENAI_API_KEY ? new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
}) : null;

class AIController {

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
      const fallback = this.generateDemoResponse(
        req.body ? req.body.message : '',
        req.user || { name: 'User', role: 'patient' }
      );
      res.status(500).json({
        error: 'Failed to generate AI response',
        message: error.message,
        fallback
      });
    }
  }

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
      max_tokens: 500,
      temperature: 0.7,
      presence_penalty: 0.1,
      frequency_penalty: 0.1
    });

    return completion.choices[0].message.content.trim();
  }

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
            text: `${systemPrompt}\n\nUser question: ${message}`
          }]
        }]
      },
      { headers: { 'Content-Type': 'application/json' } }
    );

    return response.data.candidates[0].content.parts[0].text;
  }

  async callClaude(message, user, context) {
    if (!process.env.ANTHROPIC_API_KEY) {
      throw new Error('Anthropic API key not configured');
    }

    const systemPrompt = this.createSystemPrompt(user, context);

    const response = await axios.post(
      'https://api.anthropic.com/v1/messages',
      {
        model: 'claude-3-sonnet-20240229',
        max_tokens: 500,
        messages: [
          { role: 'user', content: `${systemPrompt}\n\nUser question: ${message}` }
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

  createSystemPrompt(user, context) {
    return `You are NaturoSage, an AI-powered Homeopathy Assistant. You are knowledgeable in classical homeopathy, materia medica, repertory, and the principles of similimum.

User Context:
- Name: ${user.name}
- Role: ${user.role}
- Current Date: ${new Date().toLocaleDateString()}

Your role is to:
1. Help users understand their homeopathic constitution
2. Assist with symptom analysis using homeopathic repertory principles
3. Suggest possible homeopathic remedies based on symptom totality
4. Explain remedy pictures, modalities, and potency guidelines
5. Educate about homeopathic principles (Law of Similars, Minimum Dose, Single Remedy)
6. Always recommend consulting a qualified homeopathic practitioner for actual treatment

Important guidelines:
- Always state that AI suggestions are educational and not a substitute for professional consultation
- Use proper homeopathic terminology
- Consider the totality of symptoms
- Be warm, empathetic, and supportive
- Keep responses concise but informative (2-4 sentences typically)`;
  }

  generateDemoResponse(message, user) {
    const userName = (user.name || 'Friend').split(' ')[0];
    const lowerMessage = (message || '').toLowerCase().trim();

    if (lowerMessage.includes('constitution')) {
      return `Great question, ${userName}! In homeopathy, your constitution is your unique physical, mental, and emotional makeup. It helps determine your constitutional remedy — the remedy that matches your overall pattern. Use the Constitution Detector to discover yours!`;
    }

    if (lowerMessage.includes('potency') || lowerMessage.includes('dose')) {
      return `${userName}, potency is crucial in homeopathy. Lower potencies (6C, 12C) suit acute physical complaints, 30C is standard for general use, and higher potencies (200C, 1M) are for deep constitutional work. Always start lower and adjust based on response.`;
    }

    if (lowerMessage.includes('arnica')) {
      return `Arnica Montana is perhaps the most well-known homeopathic remedy! It's the go-to for physical trauma, bruising, muscle soreness, and post-surgical recovery. The classic keynote: the patient says "I'm fine" even when they're clearly not. Typically used in 30C for acute injuries.`;
    }

    if (['anxiety', 'anxious', 'worry', 'fear'].some(w => lowerMessage.includes(w))) {
      return `Several homeopathic remedies address anxiety, ${userName}. Aconitum for sudden panic, Arsenicum Album for restless midnight anxiety, Phosphorus for health anxiety with desire for company, and Calcarea Carb for security worries. The choice depends on your unique symptom picture.`;
    }

    if (['skin', 'eczema', 'rash', 'itch'].some(w => lowerMessage.includes(w))) {
      return `Skin conditions respond beautifully to homeopathy. Key remedies include Sulphur (burning, worse heat/bathing), Arsenicum (dry scaly, better warmth), Graphites (oozing sticky), and Natrum Mur (dry eczema at hairline). Constitutional treatment gives the best long-term results.`;
    }

    if (['digest', 'stomach', 'bloat', 'acid', 'gas'].some(w => lowerMessage.includes(w))) {
      return `Digestive complaints are very common in homeopathic practice, ${userName}. Top remedies include Nux Vomica (overindulgence, irritability), Lycopodium (bloating 4-8 PM), Pulsatilla (worse from rich food), and Arsenicum (burning pains, food poisoning).`;
    }

    if (['hello', 'hi', 'hey'].some(w => lowerMessage.includes(w))) {
      return `Hello ${userName}! I'm NaturoSage, your Homeopathy Assistant. I can help with constitution analysis, symptom checking, remedy information, and homeopathic education. What would you like to explore?`;
    }

    if (lowerMessage.includes('thank')) {
      return `You're welcome, ${userName}! Remember, homeopathy treats the whole person — mind, body, and emotions. Feel free to ask anything about remedies, constitutions, or homeopathic principles anytime!`;
    }

    if (['homeopathy', 'what is'].some(w => lowerMessage.includes(w))) {
      return `Homeopathy is a 200+ year-old natural healing system based on "Similia Similibus Curentur" — Like Cures Like. A substance causing symptoms in a healthy person can cure similar symptoms in a sick person when given in highly diluted form. It's gentle, non-toxic, and treats the whole person.`;
    }

    if (['?', 'what', 'how', 'why', 'when', 'which'].some(c => lowerMessage.includes(c))) {
      return `That's a great question, ${userName}. I can help with homeopathic remedies, constitutions, symptom analysis, potency guidance, and general principles. Could you share more details so I can give you relevant information?`;
    }

    return `I understand you're asking about "${message}", ${userName}. I'm NaturoSage, your Homeopathy Assistant. I can help with constitution analysis, symptom checking, remedy suggestions, and homeopathic education. What specific aspect would you like to explore?`;
  }

  async getProviders(req, res) {
    const providers = [
      { id: 'openai', name: 'OpenAI GPT-4', available: !!process.env.OPENAI_API_KEY },
      { id: 'gemini', name: 'Google Gemini Pro', available: !!process.env.GOOGLE_API_KEY },
      { id: 'claude', name: 'Anthropic Claude', available: !!process.env.ANTHROPIC_API_KEY },
      { id: 'demo', name: 'Demo Mode', available: true }
    ];
    res.json({ providers });
  }

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
