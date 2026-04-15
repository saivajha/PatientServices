const { v4: uuidv4 } = require('uuid');
const materiaMedicaService = require('../services/materiaMedicaService');
const medllamaClient = require('../services/medllamaClient');

const constitutionDefaults = [
  'How would you describe your body constitution: tends toward cold and dampness, heat and dryness, or mixed?',
  'How do you usually react to weather changes (cold rain, humidity, dry heat, wind)?',
  'When stressed, what mood pattern appears most (irritability, sadness, fearfulness, restlessness, withdrawal)?',
  'Do you prefer company or solitude when unwell?',
  'How are your sleep quality, dreams, and wake-up energy on most days?',
  'What are your food and drink cravings/aversions (sweet, sour, salty, warm, cold)?',
  'How sensitive are you to noise, light, smell, and touch?',
  'Do your symptoms generally improve with movement, rest, warmth, fresh air, or pressure?'
];

const symptomDefaults = [
  'What is the main complaint today, and when did it begin?',
  'Where exactly is the discomfort located, and does it spread anywhere?',
  'How would you describe the sensation (throbbing, stabbing, burning, dull, cramping, heaviness)?',
  'What makes the symptoms better or worse (time of day, food, posture, temperature, activity)?',
  'Please list associated symptoms (fever, cough, nausea, bowel changes, skin issues, fatigue, headache).',
  'On a 0-10 scale, how severe is the symptom right now and at its worst?',
  'How has this affected appetite, sleep, mood, and daily function?',
  'Have you taken any medicines/remedies so far, and what was the effect?'
];

class NaturoSageController {
  constructor() {
    this.sessions = new Map();
    this.sessionTtlMs = 6 * 60 * 60 * 1000;
  }

  async getSourceStatus(req, res) {
    try {
      const sourceStatus = await materiaMedicaService.getSourceStatus();
      res.json({
        success: true,
        sourceStatus
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: 'Failed to fetch source status.',
        message: error.message
      });
    }
  }

  async startAssessment(req, res) {
    try {
      this.cleanupExpiredSessions();

      const {
        patientName = 'Anonymous User',
        patientAge = null,
        patientSex = 'unspecified',
        provider = 'auto'
      } = req.body || {};

      const sourceStatus = await materiaMedicaService.getSourceStatus();
      const constitutionQuestions = await this.generateConstitutionQuestions({
        patientName,
        patientAge,
        patientSex,
        provider
      });

      const sessionId = uuidv4();
      const session = {
        id: sessionId,
        createdAt: Date.now(),
        updatedAt: Date.now(),
        stage: 'constitution',
        providerRequested: provider,
        llmProviderUsed: constitutionQuestions.provider,
        patientProfile: {
          patientName,
          patientAge,
          patientSex
        },
        sourceStatus,
        constitutionQuestions: constitutionQuestions.questions,
        constitutionAnswers: [],
        symptomQuestions: [],
        symptomAnswers: [],
        constitutionSummary: null,
        finalAssessment: null,
        lastWarnings: constitutionQuestions.warnings || []
      };

      this.sessions.set(sessionId, session);

      res.json({
        success: true,
        sessionId,
        stage: session.stage,
        providerUsed: session.llmProviderUsed,
        sourceStatus,
        questions: session.constitutionQuestions,
        guidance: 'Please answer each constitution question to identify the patient type before symptom analysis.'
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: 'Failed to start assessment.',
        message: error.message
      });
    }
  }

  async submitConstitution(req, res) {
    try {
      const { sessionId, answers = [], provider = 'auto' } = req.body || {};
      const session = this.getSessionOrThrow(sessionId);

      if (session.stage !== 'constitution') {
        return res.status(400).json({
          success: false,
          error: `Session is currently in "${session.stage}" stage.`
        });
      }

      if (!Array.isArray(answers) || answers.length === 0) {
        return res.status(400).json({
          success: false,
          error: 'answers must be a non-empty array.'
        });
      }

      session.constitutionAnswers = answers;
      const constitutionSummary = await this.determineConstitution({
        session,
        provider
      });
      session.constitutionSummary = constitutionSummary;

      const symptomQuestions = await this.generateSymptomQuestions({
        session,
        provider
      });
      session.symptomQuestions = symptomQuestions.questions;
      session.llmProviderUsed = symptomQuestions.provider;
      session.lastWarnings = [...(constitutionSummary.warnings || []), ...(symptomQuestions.warnings || [])];
      session.stage = 'symptoms';
      session.updatedAt = Date.now();

      res.json({
        success: true,
        stage: session.stage,
        providerUsed: session.llmProviderUsed,
        constitutionSummary: {
          type: constitutionSummary.type,
          rationale: constitutionSummary.rationale
        },
        questions: session.symptomQuestions,
        guidance: 'Please answer symptom questions in detail for remedy selection.'
      });
    } catch (error) {
      const status = /Invalid sessionId/.test(error.message) ? 404 : 500;
      res.status(status).json({
        success: false,
        error: 'Failed to submit constitution answers.',
        message: error.message
      });
    }
  }

  async submitSymptoms(req, res) {
    try {
      const { sessionId, answers = [], provider = 'auto' } = req.body || {};
      const session = this.getSessionOrThrow(sessionId);

      if (session.stage !== 'symptoms') {
        return res.status(400).json({
          success: false,
          error: `Session is currently in "${session.stage}" stage.`
        });
      }

      if (!Array.isArray(answers) || answers.length === 0) {
        return res.status(400).json({
          success: false,
          error: 'answers must be a non-empty array.'
        });
      }

      session.symptomAnswers = answers;
      const finalAssessment = await this.generateFinalAssessment({
        session,
        provider
      });
      session.finalAssessment = finalAssessment;
      session.llmProviderUsed = finalAssessment.provider;
      session.lastWarnings = finalAssessment.warnings || [];
      session.stage = 'completed';
      session.updatedAt = Date.now();

      res.json({
        success: true,
        stage: session.stage,
        providerUsed: session.llmProviderUsed,
        assessment: finalAssessment.data,
        warnings: finalAssessment.warnings || [],
        note: 'For education support only. Any diagnosis or medicine decision must be confirmed by a qualified clinician.'
      });
    } catch (error) {
      const status = /Invalid sessionId/.test(error.message) ? 404 : 500;
      res.status(status).json({
        success: false,
        error: 'Failed to submit symptom answers.',
        message: error.message
      });
    }
  }

  async getSession(req, res) {
    try {
      const { sessionId } = req.params;
      const session = this.getSessionOrThrow(sessionId);
      res.json({
        success: true,
        session: this.presentSession(session)
      });
    } catch (error) {
      const status = /Invalid sessionId/.test(error.message) ? 404 : 500;
      res.status(status).json({
        success: false,
        error: error.message
      });
    }
  }

  getSessionOrThrow(sessionId) {
    if (!sessionId) {
      throw new Error('Invalid sessionId: missing.');
    }
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error('Invalid sessionId: session not found.');
    }
    return session;
  }

  presentSession(session) {
    return {
      id: session.id,
      stage: session.stage,
      createdAt: session.createdAt,
      updatedAt: session.updatedAt,
      providerRequested: session.providerRequested,
      llmProviderUsed: session.llmProviderUsed,
      patientProfile: session.patientProfile,
      sourceStatus: session.sourceStatus,
      constitutionQuestions: session.constitutionQuestions,
      constitutionAnswers: session.constitutionAnswers,
      constitutionSummary: session.constitutionSummary,
      symptomQuestions: session.symptomQuestions,
      symptomAnswers: session.symptomAnswers,
      finalAssessment: session.finalAssessment ? session.finalAssessment.data : null,
      warnings: session.lastWarnings || []
    };
  }

  cleanupExpiredSessions() {
    const now = Date.now();
    for (const [id, session] of this.sessions.entries()) {
      if ((now - session.updatedAt) > this.sessionTtlMs) {
        this.sessions.delete(id);
      }
    }
  }

  formatQnA(questions, answers) {
    return questions
      .map((question, index) => {
        const answer = answers[index] || '(no answer)';
        return `${index + 1}. Q: ${question}\nA: ${answer}`;
      })
      .join('\n\n');
  }

  extractJson(text) {
    if (!text) {
      return null;
    }
    const match = text.match(/\{[\s\S]*\}/);
    if (!match) {
      return null;
    }
    try {
      return JSON.parse(match[0]);
    } catch (error) {
      return null;
    }
  }

  async llmJson({
    provider,
    systemPrompt,
    userPrompt,
    fallback,
    maxTokens = 1400
  }) {
    const completion = await medllamaClient.complete({
      provider,
      systemPrompt,
      userPrompt,
      maxTokens,
      temperature: 0.2
    });

    if (!completion.text) {
      return {
        json: fallback,
        provider: completion.provider,
        warnings: completion.error ? [completion.error] : ['LLM response unavailable; fallback used.']
      };
    }

    const parsed = this.extractJson(completion.text);
    if (!parsed) {
      return {
        json: fallback,
        provider: completion.provider,
        warnings: ['LLM response was not valid JSON; fallback used.']
      };
    }

    return {
      json: parsed,
      provider: completion.provider,
      warnings: []
    };
  }

  async generateConstitutionQuestions({ patientName, patientAge, patientSex, provider }) {
    const fallback = { questions: constitutionDefaults };
    const systemPrompt = [
      'You are NaturoSage, a careful homoeopathy intake assistant.',
      'Generate exactly 8 concise intake questions to determine constitutional type (hydrogenoid, oxygenoid, or mixed).',
      'Focus on temperament, modalities, environmental sensitivity, cravings, sleep, behavior, and general disposition.',
      'Respond as strict JSON only in format {"questions":["..."]}.'
    ].join(' ');

    const userPrompt = `Patient profile: name=${patientName}, age=${patientAge || 'unknown'}, sex=${patientSex}.`;
    const result = await this.llmJson({
      provider,
      systemPrompt,
      userPrompt,
      fallback,
      maxTokens: 700
    });

    const questions = Array.isArray(result.json.questions) && result.json.questions.length
      ? result.json.questions.slice(0, 8).map((question) => String(question))
      : constitutionDefaults;

    return {
      questions,
      provider: result.provider,
      warnings: result.warnings
    };
  }

  async determineConstitution({ session, provider }) {
    const fallback = {
      type: 'mixed',
      confidence: 0.35,
      rationale: 'Fallback summary used due to unavailable structured LLM output.',
      keyTraits: ['Insufficient structured data'],
      cautions: ['Assessment requires human homoeopathic practitioner confirmation.']
    };

    const qna = this.formatQnA(session.constitutionQuestions, session.constitutionAnswers);
    const systemPrompt = [
      'You are NaturoSage and must classify constitution using only provided Q/A.',
      'Possible type values: "hydrogenoid", "oxygenoid", "mixed".',
      'Respond as strict JSON:',
      '{"type":"...", "confidence":0.0, "rationale":"...", "keyTraits":["..."], "cautions":["..."]}'
    ].join(' ');
    const userPrompt = `Patient: ${JSON.stringify(session.patientProfile)}\n\nConstitution Q/A:\n${qna}`;

    const result = await this.llmJson({
      provider,
      systemPrompt,
      userPrompt,
      fallback,
      maxTokens: 900
    });

    const normalizedType = ['hydrogenoid', 'oxygenoid', 'mixed'].includes(result.json.type)
      ? result.json.type
      : 'mixed';

    return {
      type: normalizedType,
      confidence: Number(result.json.confidence || 0),
      rationale: String(result.json.rationale || fallback.rationale),
      keyTraits: Array.isArray(result.json.keyTraits) ? result.json.keyTraits.map((item) => String(item)) : fallback.keyTraits,
      cautions: Array.isArray(result.json.cautions) ? result.json.cautions.map((item) => String(item)) : fallback.cautions,
      warnings: result.warnings
    };
  }

  async generateSymptomQuestions({ session, provider }) {
    const fallback = { questions: symptomDefaults };
    const systemPrompt = [
      'You are NaturoSage and need symptom differentiation questions after constitutional typing.',
      'Generate exactly 8 concise follow-up symptom questions to support provisional diagnosis and remedy matching.',
      'Questions should cover onset, location, sensation, modalities, concomitants, severity, chronology, and prior response.',
      'Respond as strict JSON only {"questions":["..."]}.'
    ].join(' ');

    const userPrompt = [
      `Patient profile: ${JSON.stringify(session.patientProfile)}.`,
      `Constitution summary: ${JSON.stringify(session.constitutionSummary)}.`
    ].join('\n');

    const result = await this.llmJson({
      provider,
      systemPrompt,
      userPrompt,
      fallback,
      maxTokens: 700
    });

    const questions = Array.isArray(result.json.questions) && result.json.questions.length
      ? result.json.questions.slice(0, 8).map((question) => String(question))
      : symptomDefaults;

    return {
      questions,
      provider: result.provider,
      warnings: result.warnings
    };
  }

  async generateFinalAssessment({ session, provider }) {
    const symptomQnA = this.formatQnA(session.symptomQuestions, session.symptomAnswers);
    const constitutionQnA = this.formatQnA(session.constitutionQuestions, session.constitutionAnswers);

    const retrievalQuery = [
      session.constitutionSummary?.type || '',
      session.constitutionSummary?.keyTraits?.join(' ') || '',
      session.symptomAnswers.join(' ')
    ].join(' ');

    const retrieval = await materiaMedicaService.searchContext(retrievalQuery, 6);
    const passageText = retrieval.passages
      .map((passage, index) => `[${index + 1}] ${passage.citation}\n${passage.excerpt}`)
      .join('\n\n');

    const fallback = {
      diagnosis: {
        summary: 'Unable to generate structured provisional diagnosis from model.',
        differential: ['Needs clinician review'],
        confidence: 0.2
      },
      constitutionalType: session.constitutionSummary?.type || 'mixed',
      remedyPlan: [
        {
          name: 'Remedy selection pending',
          rationale: 'LLM output unavailable; manual practitioner review required.',
          suggestedPotency: 'N/A',
          dosingNotes: 'N/A'
        }
      ],
      followUpQuestions: [],
      redFlags: ['Escalate to licensed clinician for diagnosis confirmation.'],
      safetyDisclaimer: 'Educational support only. Not a medical diagnosis or treatment prescription.'
    };

    const systemPrompt = [
      'You are NaturoSage, an evidence-grounded homoeopathy triage copilot.',
      'Use ONLY provided patient data and Materia Medica excerpts. Do not invent citations.',
      'Return strict JSON:',
      '{"diagnosis":{"summary":"...","differential":["..."],"confidence":0.0},',
      '"constitutionalType":"hydrogenoid|oxygenoid|mixed",',
      '"remedyPlan":[{"name":"...","rationale":"...","suggestedPotency":"...","dosingNotes":"..."}],',
      '"followUpQuestions":["..."],',
      '"redFlags":["..."],',
      '"safetyDisclaimer":"..."}'
    ].join(' ');

    const userPrompt = [
      `Patient profile: ${JSON.stringify(session.patientProfile)}`,
      `Constitution summary: ${JSON.stringify(session.constitutionSummary)}`,
      '',
      'Constitution Q/A:',
      constitutionQnA,
      '',
      'Symptom Q/A:',
      symptomQnA,
      '',
      'Materia Medica excerpts:',
      passageText || 'No passages found.'
    ].join('\n');

    const modelResult = await this.llmJson({
      provider,
      systemPrompt,
      userPrompt,
      fallback,
      maxTokens: 1800
    });

    const assessment = modelResult.json || fallback;
    const remedyPlan = Array.isArray(assessment.remedyPlan) ? assessment.remedyPlan : fallback.remedyPlan;
    const differential = Array.isArray(assessment.differential)
      ? assessment.differential
      : (assessment.diagnosis && Array.isArray(assessment.diagnosis.differential)
        ? assessment.diagnosis.differential
        : fallback.diagnosis.differential);

    const normalized = {
      diagnosis: {
        summary: String(assessment.diagnosis?.summary || fallback.diagnosis.summary),
        differential: differential.map((item) => String(item)).slice(0, 5),
        confidence: Number(assessment.diagnosis?.confidence || fallback.diagnosis.confidence)
      },
      constitutionalType: ['hydrogenoid', 'oxygenoid', 'mixed'].includes(assessment.constitutionalType)
        ? assessment.constitutionalType
        : (session.constitutionSummary?.type || 'mixed'),
      remedyPlan: remedyPlan.slice(0, 5).map((item) => ({
        name: String(item.name || 'Unnamed remedy'),
        rationale: String(item.rationale || 'No rationale provided.'),
        suggestedPotency: String(item.suggestedPotency || 'Not specified'),
        dosingNotes: String(item.dosingNotes || 'Not specified')
      })),
      followUpQuestions: Array.isArray(assessment.followUpQuestions)
        ? assessment.followUpQuestions.slice(0, 8).map((item) => String(item))
        : [],
      redFlags: Array.isArray(assessment.redFlags)
        ? assessment.redFlags.slice(0, 8).map((item) => String(item))
        : fallback.redFlags,
      safetyDisclaimer: String(assessment.safetyDisclaimer || fallback.safetyDisclaimer),
      citations: retrieval.passages.map((passage) => ({
        citation: passage.citation,
        sourcePath: passage.sourcePath,
        excerpt: passage.excerpt
      }))
    };

    return {
      provider: modelResult.provider,
      data: normalized,
      warnings: [...(retrieval.warnings || []), ...(modelResult.warnings || [])]
    };
  }
}

module.exports = new NaturoSageController();
