const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const pdfParse = require('pdf-parse');
const { LocalEmbeddings, LocalIndex } = require('vectra');

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
    this.lastFingerprint = '';

    this.vectorEnabled = (process.env.MATERIA_MEDICA_ENABLE_VECTOR || 'true') !== 'false';
    this.vectorIndexPath = path.resolve(
      process.env.MATERIA_MEDICA_VECTOR_DIR || path.join(process.cwd(), '.vectordb', 'materia-medica')
    );
    this.vectorManifestPath = path.join(this.vectorIndexPath, 'manifest.json');
    this.embeddingModelName = process.env.MATERIA_MEDICA_EMBEDDING_MODEL || 'Xenova/all-MiniLM-L6-v2';
    this.vectorIndexVersion = 1;

    this.embeddings = null;
    this.index = null;
    this.vectorInitPromise = null;
    this.vectorState = {
      ready: false,
      indexedItems: 0,
      lastBuildAt: null,
      lastError: null
    };
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
        const stats = await fs.promises.stat(filePath);
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
          sizeBytes: stats.size,
          mtimeMs: Math.round(stats.mtimeMs),
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
    this.lastFingerprint = this.computeFingerprint(loadedDocuments);

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

  computeFingerprint(documents) {
    const serialized = JSON.stringify(
      documents.map((doc) => ({
        sourcePath: doc.sourcePath,
        sizeBytes: doc.sizeBytes || 0,
        mtimeMs: doc.mtimeMs || 0,
        chunkCount: doc.chunkCount || 0
      }))
    );
    return crypto.createHash('sha256').update(serialized).digest('hex');
  }

  getVectorStatus() {
    return {
      enabled: this.vectorEnabled,
      indexPath: this.vectorIndexPath,
      embeddingModel: this.embeddingModelName,
      ...this.vectorState
    };
  }

  async ensureEmbeddingsModel() {
    if (!this.embeddings) {
      this.embeddings = new LocalEmbeddings({
        model: this.embeddingModelName,
        maxTokens: 256
      });
    }
    return this.embeddings;
  }

  async readManifest() {
    try {
      const content = await fs.promises.readFile(this.vectorManifestPath, 'utf8');
      return JSON.parse(content);
    } catch (error) {
      return null;
    }
  }

  async writeManifest(data) {
    await fs.promises.mkdir(this.vectorIndexPath, { recursive: true });
    await fs.promises.writeFile(this.vectorManifestPath, JSON.stringify(data, null, 2), 'utf8');
  }

  async ensureVectorIndex({ forceRebuild = false } = {}) {
    if (!this.vectorEnabled) {
      return { warnings: ['Vector retrieval disabled by MATERIA_MEDICA_ENABLE_VECTOR=false.'] };
    }

    if (this.chunks.length === 0) {
      this.vectorState.ready = false;
      this.vectorState.indexedItems = 0;
      return { warnings: ['No chunks available to build vector index.'] };
    }

    if (!forceRebuild && this.vectorInitPromise) {
      return this.vectorInitPromise;
    }

    this.vectorInitPromise = this.initializeOrRefreshVectorIndex({ forceRebuild })
      .finally(() => {
        this.vectorInitPromise = null;
      });
    return this.vectorInitPromise;
  }

  async initializeOrRefreshVectorIndex({ forceRebuild = false } = {}) {
    const warnings = [];
    try {
      this.index = new LocalIndex(this.vectorIndexPath);
      const indexExists = await this.index.isIndexCreated();
      const manifest = await this.readManifest();
      const shouldRebuild = forceRebuild
        || !indexExists
        || !manifest
        || manifest.fingerprint !== this.lastFingerprint
        || manifest.embeddingModel !== this.embeddingModelName
        || manifest.indexVersion !== this.vectorIndexVersion
        || manifest.chunkCount !== this.chunks.length;

      if (shouldRebuild) {
        await this.index.createIndex({
          version: this.vectorIndexVersion,
          deleteIfExists: true
        });

        const embeddings = await this.ensureEmbeddingsModel();
        await this.index.beginUpdate();

        try {
          const batchSize = 12;
          for (let start = 0; start < this.chunks.length; start += batchSize) {
            const batch = this.chunks.slice(start, start + batchSize);
            const textBatch = batch.map((chunk) => chunk.text);
            const embeddingResponse = await embeddings.createEmbeddings(textBatch);
            if (embeddingResponse.status !== 'success') {
              throw new Error(embeddingResponse.message || 'Embedding generation failed.');
            }

            for (let i = 0; i < batch.length; i += 1) {
              const chunk = batch[i];
              const vector = embeddingResponse.output[i];

              await this.index.insertItem({
                id: chunk.id,
                vector,
                metadata: {
                  citation: `${chunk.sourceLabel}#${chunk.chunkIndex + 1}`,
                  sourceLabel: chunk.sourceLabel,
                  sourcePath: chunk.sourcePath,
                  chunkIndex: chunk.chunkIndex,
                  excerpt: chunk.text.slice(0, 700)
                }
              });
            }
          }
          await this.index.endUpdate();
        } catch (error) {
          this.index.cancelUpdate();
          throw error;
        }

        await this.writeManifest({
          indexVersion: this.vectorIndexVersion,
          embeddingModel: this.embeddingModelName,
          fingerprint: this.lastFingerprint,
          chunkCount: this.chunks.length,
          updatedAt: new Date().toISOString()
        });
      }

      const stats = await this.index.getIndexStats();
      this.vectorState.ready = true;
      this.vectorState.indexedItems = stats.items;
      this.vectorState.lastBuildAt = new Date().toISOString();
      this.vectorState.lastError = null;
      return { warnings };
    } catch (error) {
      this.vectorState.ready = false;
      this.vectorState.lastError = error.message;
      warnings.push(`Vector index unavailable: ${error.message}`);
      return { warnings };
    }
  }

  async buildVectorIndex({ forceRebuild = true } = {}) {
    await this.ensureLoaded();
    const build = await this.ensureVectorIndex({ forceRebuild });
    return {
      success: this.vectorState.ready,
      ...this.getVectorStatus(),
      warnings: [...this.loadWarnings, ...(build.warnings || [])]
    };
  }

  async getSourceStatus() {
    await this.ensureLoaded();
    const vectorStatus = this.getVectorStatus();
    return {
      configuredPaths: this.paths,
      documentCount: this.documents.length,
      chunkCount: this.chunks.length,
      documents: this.documents,
      vector: vectorStatus,
      warnings: this.loadWarnings
    };
  }

  async searchContext(query, limit = 6) {
    await this.ensureLoaded();
    const warnings = [...this.loadWarnings];

    if (this.chunks.length === 0) {
      return {
        passages: [],
        warnings: this.loadWarnings.length
          ? this.loadWarnings
          : ['No Materia Medica documents are available for retrieval.']
      };
    }

    const queryText = (query || '').trim();
    const queryTokens = this.tokenize(queryText);
    if (!queryText || queryTokens.length === 0) {
      return { passages: [], warnings, retrievalMode: 'none' };
    }

    if (this.vectorEnabled) {
      const vectorInit = await this.ensureVectorIndex({ forceRebuild: false });
      warnings.push(...(vectorInit.warnings || []));

      if (this.vectorState.ready && this.index) {
        try {
          const embeddings = await this.ensureEmbeddingsModel();
          const embeddingResponse = await embeddings.createEmbeddings(queryText);
          if (embeddingResponse.status !== 'success') {
            throw new Error(embeddingResponse.message || 'Failed to embed query text.');
          }

          const queryVector = embeddingResponse.output[0];
          const rawResults = await this.index.queryItems(
            queryVector,
            queryText,
            Math.max(limit * 2, limit),
            undefined,
            true
          );

          const unique = new Map();
          for (const result of rawResults) {
            if (!result || !result.item) {
              continue;
            }
            if (!unique.has(result.item.id)) {
              unique.set(result.item.id, result);
            }
          }

          const passages = Array.from(unique.values())
            .sort((a, b) => b.score - a.score)
            .slice(0, limit)
            .map((result) => ({
              citation: result.item.metadata?.citation || result.item.id,
              sourcePath: result.item.metadata?.sourcePath || '',
              excerpt: result.item.metadata?.excerpt || '',
              score: Number(result.score || 0)
            }));

          if (passages.length > 0) {
            return {
              passages,
              warnings,
              retrievalMode: 'vector'
            };
          }
        } catch (error) {
          warnings.push(`Vector search failed, using keyword fallback: ${error.message}`);
        }
      }
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
      warnings,
      retrievalMode: 'keyword'
    };
  }
}

module.exports = new MateriaMedicaService();
