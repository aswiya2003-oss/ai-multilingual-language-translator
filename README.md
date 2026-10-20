# AI-Based Multilingual Language Translation System

Final-year project prototype for text, voice, and document translation.

## 1. Features

- Multilingual text translation using NLLB-200 distilled 600M.
- Voice transcription using OpenAI Whisper, followed by translation.
- TXT, DOCX, and text-based PDF extraction.
- Download translated output as TXT or DOCX.
- BLEU and chrF evaluation helper.
- Streamlit user interface.

## 2. Requirements

- Python 3.10 or 3.11 recommended.
- Internet access for first-time model downloads.
- RAM/storage: the translation and speech models are large; 8 GB RAM is a practical minimum, and more is recommended. GPU is optional but improves speed.
- Audio decoding may require FFmpeg, depending on your environment.

## 3. Setup

### Windows (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

### Linux/macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501).

## 4. Model details

- Translation model: `facebook/nllb-200-distilled-600M`
- Speech recognition model: `openai/whisper-small`
- NLLB uses language tags such as `eng_Latn`, `tel_Telu`, and `hin_Deva`.
- This implementation uses pretrained inference. It does not claim the model was trained from scratch.
- Check the current model-card license and usage conditions before deployment or redistribution. NLLB research models may have non-commercial restrictions.

## 5. Supported language choices

The interface offers English, Telugu, Hindi, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Urdu, French, Spanish, German, Portuguese, Arabic, Simplified Chinese, Japanese, Korean, and Russian. Availability and quality vary by language pair. If a pair fails, verify the model's current language codes and tokenizer support.

## 6. Voice workflow

1. Upload WAV, MP3, M4A, OGG, or FLAC audio.
2. Whisper converts speech into text.
3. Confirm the source language shown in the interface.
4. Select the target language and translate.
5. Download the translated transcript.

Speech recognition is a separate model from translation. Automatic language detection can be imperfect, so review the transcript.

## 7. Document workflow

1. Upload TXT, DOCX, or text-based PDF.
2. Select source and target languages.
3. Extract text and translate it in chunks.
4. Preview and download TXT or DOCX output.

Limitations: PDF layout, images, tables, headers, footers, and complex formatting may not be preserved. Scanned PDFs need OCR, which is not included in this starter version. Long documents can take time and may need chunk-size tuning.

## 8. Evaluation plan

Create a held-out dataset of at least 50–200 source sentences for each language pair. Obtain high-quality human reference translations. Run the same sentences through the system and save one hypothesis per line.

```bash
python evaluate_bleu.py references.txt hypotheses.txt
```

Report:
- BLEU and chrF by language pair.
- Mean and median latency per sentence.
- Number of test sentences and hardware used.
- Human ratings for adequacy and fluency (1–5).
- Error examples: named entities, idioms, grammar, domain terminology, and code-mixed text.

Do not invent scores. Run the evaluation and report actual results, including test-set size and conditions. BLEU is not a complete measure of translation quality.

## 9. Suggested final-year enhancements

- Fine-tune a supported model on a licensed parallel corpus.
- Add OCR for scanned PDFs.
- Preserve document structure and tables.
- Add text-to-speech playback for translated output.
- Add translation history with user consent and secure storage.
- Add confidence warnings and a manual correction workflow.
- Compare NLLB with another multilingual model under the same evaluation setup.

## 10. Troubleshooting

- **First run is slow:** models are downloading; wait for completion.
- **Out of memory:** use a smaller supported model, reduce input length, or run on a machine with more RAM.
- **Audio decode error:** install FFmpeg and restart the terminal.
- **PDF has no extracted text:** likely scanned; use OCR before upload.
- **Language pair output looks wrong:** check the selected source language and NLLB language tags.
- **Model download/access failure:** verify internet connectivity, package versions, and model repository availability.

## 11. Academic integrity

This is a starter implementation using existing pretrained models. In your report, clearly identify pretrained components, datasets, model licenses, your own implementation, and your measured results. Do not describe pretrained inference as training a model from scratch.
