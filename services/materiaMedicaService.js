const fs = require('fs');
const path = require('path');
const pdfParse = require('pdf-parse');

const DEFAULT_MATERIA_MEDICA_PATHS = [
  '/Applications/HomeoSage/MateriaMedica/MateriaMedicaVol1.pdf',
  '/Applications/HomeoSage/MateriaMedica/MateriaMedicaVol2.pdf',
  '/Applications/HomeoSage/MateriaMedica/MateriaMedicaVol3.pdf',
  '/Applications/HomeoSage/MateriaMedica/MateriaMedicaVol4.pdf'
];

class MateriaMedicaService {
  constructor() {
    this.paths = (process.env.MATERIA_MEDICA_PATHS || '')
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);

    if (this.paths.length === 0) {
      this.paths = DEFAULT_MATERIA_MEDICA_PATHS;
    }

    this.documents = [];
    this.chunks = [];
    this.loadWarnings = [];
    this.initPromise = null;
  }

  async ensureLoaded() {
    if (!this.initPromise) {
      this.initPromise = this.loadDocuments();
    }

    return this.initPromise;
  }

  async loadDocuments() {
    const loadedDocuments = [];
    const loadedChunks = [];
    const warnings = [];

    for (const filePath of this.paths) {
      try {
        await fs.promises.access(filePath, fs.constants.R_OK);
        const pdfBuffer = await fs.promises.readFile(filePath);
        const parsed = await pdfParse(pdfBuffer);

        const text = this.normalizeText(parsed.text || '');
        if (!text) {
          warnings.push(`No extractable text in ${filePath}`);
          continue;
        }

        const sourceLabel = path.basename(filePath);
        const docId = `${sourceLabel}-${loadedDocuments.length + 1}`;
        const chunks = this.chunkText(text, 1400);

        loadedDocuments.push({
          id: docId,
          sourcePath: filePath,
          sourceLabel,
          charCount: text.length,
          chunkCount: chunks.length
        });

        chunks.forEach((chunkText, index) => {
          loadedChunks.push({
            id: `${docId}-chunk-${index + 1}`,
            sourcePath: filePath,
            sourceLabel,
            chunkIndex: index,
            text: chunkText,
            normalized: chunkText.toLowerCase()
          });
        });
      } catch (error) {
        warnings.push(`Failed to load ${filePath}: ${error.message}`);
      }
    }

    this.documents = loadedDocuments;
    this.chunks = loadedChunks;
    this.loadWarnings = warnings;

    return {
      documents: this.documents,
      chunkCount: this.chunks.length,
      warnings: this.loadWarnings
    };
  }

  normalizeText(text) {
    return text
      .replace(/\r/g, '\n')
      .replace(/\n{3,}/g, '\n\n')
      .replace(/[ \t]+/g, ' ')
      .split('\n')
      .map((line) => line.trim())
      .join('\n')
      .trim();
  }

  chunkText(text, maxChars = 1400) {
    const paragraphs = text
      .split(/\n{2,}/)
      .map((paragraph) => paragraph.trim())
      .filter((paragraph) => paragraph.length > 50);

    if (paragraphs.length === 0) {
      return this.splitByLength(text, maxChars);
    }

    const chunks = [];
    let buffer = '';

    for (const paragraph of paragraphs) {
      if (!buffer) {
        buffer = paragraph;
        continue;
      }

      if ((buffer.length + paragraph.length + 1) <= maxChars) {
        buffer += ` ${paragraph}`;
      } else {
        chunks.push(buffer);
        buffer = paragraph;
      }
    }

    if (buffer) {
      chunks.push(buffer);
    }

    return chunks;
  }

  splitByLength(text, maxChars) {
    const chunks = [];
    for (let index = 0; index < text.length; index += maxChars) {
      chunks.push(text.slice(index, index + maxChars));
    }
    return chunks;
  }

  tokenize(text) {
    return (text.toLowerCase().match(/[a-z0-9]+/g) || [])
      .filter((token) => token.length > 2);
  }

  scoreChunk(chunk, queryTokens) {
    let score = 0;
    for (const token of queryTokens) {
      const regex = new RegExp(`\\b${this.escapeRegExp(token)}\\b`, 'g');
      const matches = chunk.normalized.match(regex);
      if (matches) {
        score += Math.min(matches.length, 8);
      }
    }
    return score;
  }

  escapeRegExp(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  async getSourceStatus() {
    await this.ensureLoaded();
    return {
      configuredPaths: this.paths,
      documentCount: this.documents.length,
      chunkCount: this.chunks.length,
      documents: this.documents,
      warnings: this.loadWarnings
    };
  }

  async searchContext(query, limit = 6) {
    await this.ensureLoaded();

    if (this.chunks.length === 0) {
      return {
        passages: [],
        warnings: this.loadWarnings.length
          ? this.loadWarnings
          : ['No Materia Medica documents are available for retrieval.']
      };
    }

    const queryTokens = this.tokenize(query);
    if (queryTokens.length === 0) {
      return { passages: [], warnings: [] };
    }

    const ranked = this.chunks
      .map((chunk) => ({
        ...chunk,
        score: this.scoreChunk(chunk, queryTokens)
      }))
      .filter((chunk) => chunk.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);

    const passages = ranked.map((chunk) => ({
      citation: `${chunk.sourceLabel}#${chunk.chunkIndex + 1}`,
      sourcePath: chunk.sourcePath,
      excerpt: chunk.text.slice(0, 700),
      score: chunk.score
    }));

    return {
      passages,
      warnings: this.loadWarnings
    };
  }
}

module.exports = new MateriaMedicaService();
