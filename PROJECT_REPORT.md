# AI-Based Multilingual Language Translation System
## Final-Year Project Report (Editable Draft)

### Abstract
Language differences create barriers in education, travel, public services, and digital communication. This project develops a multilingual translation prototype that accepts typed text, audio recordings, and common text documents. A pretrained neural machine translation model translates text between selected languages. For audio, an automatic speech recognition model generates a transcript before translation. For documents, text is extracted from TXT, DOCX, or text-based PDF files and translated in chunks. A web interface provides language selection, previews, and downloadable results. The project also defines an evaluation methodology using BLEU, chrF, latency measurements, and human assessment. Since pretrained models can produce errors and language-pair performance varies, outputs should be reviewed for important uses.

### 1. Introduction
Machine translation uses computational methods to convert meaning from a source language into a target language. Neural machine translation models learn representations of context and generate target-language sequences. Modern multilingual models can handle many language pairs with a shared model, although performance varies with training-data availability, domain, and script.

### 2. Problem Statement
Manual translation can be slow and expensive for routine communication. A useful prototype should provide a common interface for text, voice recordings, and document text while allowing users to select languages and export translations.

### 3. Objectives
1. Implement a multilingual text translation interface.
2. Integrate speech-to-text and translate recognized speech.
3. Extract text from TXT, DOCX, and text-based PDF documents.
4. Export translations in TXT and DOCX formats.
5. Evaluate output quality and latency on a documented test set.
6. Identify limitations and ethical considerations.

### 4. Proposed System
The system has four main modules:
- User interface: Streamlit.
- Translation: NLLB-200 distilled 600M via Transformers.
- Speech recognition: Whisper via Transformers.
- Document processing: python-docx and PyMuPDF.

Text flow: user input → source/target language selection → translation model → result preview/export.

Voice flow: audio upload → speech recognition → transcript review/source-language confirmation → translation model → result export.

Document flow: file upload → text extraction → paragraph/sentence chunking → translation model → preview and export.

### 5. Methodology
The implementation loads pretrained models and performs inference. The source language is set using the model's language tag, and the target language is specified during generation. Long document text is split into smaller chunks to reduce input-length problems. Audio is transcribed separately because speech recognition and translation are different tasks.

### 6. Software and Hardware Requirements
Software: Python 3.10/3.11, Streamlit, PyTorch, Transformers, SentencePiece, Whisper, python-docx, PyMuPDF, SacreBLEU.

Hardware: a modern CPU, 8 GB RAM as a practical starting point, sufficient storage for model weights, and internet access for initial downloads. A supported GPU is optional.

### 7. Implementation
The application is divided into:
- `app.py`: user interface and workflow.
- `translator.py`: translation model and language mapping.
- `speech.py`: audio transcription.
- `documents.py`: text extraction and DOCX generation.
- `evaluate_bleu.py`: BLEU/chrF evaluation.

Installation and execution steps are documented in README.md.

### 8. Testing Plan
Test each module independently and end-to-end:
1. Empty input and same-language input.
2. Short and long paragraphs.
3. Every intended language pair.
4. Clear and noisy audio recordings.
5. TXT, DOCX, text-based PDF, and scanned PDF behavior.
6. Invalid file types and model-loading errors.
7. Output download and Unicode rendering.
8. CPU/GPU latency and memory use.

### 9. Evaluation
Prepare aligned source sentences, human references, and system hypotheses. Use SacreBLEU to calculate BLEU and chrF. Record model version, language pair, test set size, hardware, and runtime. Ask fluent speakers to rate adequacy and fluency from 1 to 5. Include examples of both successful translations and errors. No results should be claimed until experiments have actually been run.

Results table template:

| Language pair | Test samples | BLEU | chrF | Avg. latency (s) | Human rating |
|---|---:|---:|---:|---:|---:|
| English → Telugu | To measure | To measure | To measure | To measure | To measure |
| English → Hindi | To measure | To measure | To measure | To measure | To measure |
| English → Tamil | To measure | To measure | To measure | To measure | To measure |

### 10. Advantages
- One interface for several translation workflows.
- Reuses pretrained models, reducing training requirements.
- Handles multiple scripts when supported by the model.
- Supports downloadable output and reproducible evaluation.

### 11. Limitations
- Translation quality varies by language pair and domain.
- First-time downloads and inference require substantial resources.
- Speech recognition may mishear accents, background noise, or code-switching.
- PDF text extraction does not preserve complex layouts and does not perform OCR.
- Chunking can lose context across boundaries.
- BLEU and chrF do not fully represent meaning or usefulness.
- Model license and intended-use restrictions must be checked before deployment.

### 12. Future Scope
- Fine-tuning on appropriately licensed parallel corpora.
- OCR for scanned documents.
- Text-to-speech for translated results.
- Better layout preservation for Word/PDF files.
- Domain-specific translation and terminology glossaries.
- Secure history, authentication, and privacy controls.
- Comparison of several models under a common test protocol.

### 13. Conclusion
The project demonstrates a practical multilingual translation pipeline for text, speech transcripts, and document text. It integrates pretrained neural translation and speech recognition models into a web interface. The implementation is suitable as a base for final-year experimentation, but model performance must be measured and reported honestly. Further work can focus on evaluation, fine-tuning, OCR, speech output, and improved document formatting.

### References
1. NLLB Team et al., “No Language Left Behind: Scaling Human-Centered Machine Translation,” Meta AI, 2022. Consult the paper and model card for current technical and licensing details.
2. Hugging Face Transformers documentation: https://huggingface.co/docs/transformers
3. NLLB-200 distilled 600M model card: https://huggingface.co/facebook/nllb-200-distilled-600M
4. OpenAI Whisper repository: https://github.com/openai/whisper
5. SacreBLEU repository: https://github.com/mjpost/sacrebleu
6. Streamlit documentation: https://docs.streamlit.io/
