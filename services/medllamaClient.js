const OpenAI = require('openai');

class MedLlamaClient {
  constructor() {
    this.medllamaModel = process.env.MEDLLAMA_MODEL || 'medllama';
    this.medllamaBaseUrl = process.env.MEDLLAMA_BASE_URL || '';
    this.medllamaApiKey = process.env.MEDLLAMA_API_KEY || '';

    this.openAiModel = process.env.OPENAI_MODEL || 'gpt-4o-mini';
    this.openAiApiKey = process.env.OPENAI_API_KEY || '';

    this.medllamaClient = this.medllamaBaseUrl
      ? new OpenAI({
        baseURL: this.medllamaBaseUrl,
        apiKey: this.medllamaApiKey || 'not-required'
      })
      : null;

    this.openAiClient = this.openAiApiKey
      ? new OpenAI({ apiKey: this.openAiApiKey })
      : null;
  }

  async complete({
    systemPrompt,
    userPrompt,
    temperature = 0.2,
    maxTokens = 1000,
    provider = 'medllama'
  }) {
    const providerOrder = this.resolveProviderOrder(provider);

    let lastError = null;
    for (const item of providerOrder) {
      try {
        if (item === 'medllama' && this.medllamaClient) {
          const response = await this.medllamaClient.chat.completions.create({
            model: this.medllamaModel,
            messages: [
              { role: 'system', content: systemPrompt },
              { role: 'user', content: userPrompt }
            ],
            temperature,
            max_tokens: maxTokens
          });

          return {
            text: response.choices[0]?.message?.content?.trim() || '',
            provider: 'medllama'
          };
        }

        if (item === 'openai' && this.openAiClient) {
          const response = await this.openAiClient.chat.completions.create({
            model: this.openAiModel,
            messages: [
              { role: 'system', content: systemPrompt },
              { role: 'user', content: userPrompt }
            ],
            temperature,
            max_tokens: maxTokens
          });

          return {
            text: response.choices[0]?.message?.content?.trim() || '',
            provider: 'openai'
          };
        }
      } catch (error) {
        lastError = error;
      }
    }

    return {
      text: '',
      provider: 'none',
      error: lastError ? lastError.message : 'No configured LLM provider is available.'
    };
  }

  resolveProviderOrder(provider) {
    if (provider === 'openai') {
      return ['openai', 'medllama'];
    }

    if (provider === 'auto') {
      return ['medllama', 'openai'];
    }

    return ['medllama', 'openai'];
  }
}

module.exports = new MedLlamaClient();
