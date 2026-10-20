import os
import tempfile
from pathlib import Path

import streamlit as st
from translator import TranslationEngine, SUPPORTED_LANGUAGES
from speech import transcribe_audio
from documents import extract_text, make_docx

st.set_page_config(page_title="AI Multilingual Translator", page_icon="🌐", layout="wide")
st.title("🌐 AI-Based Multilingual Language Translation")
st.caption("Final-year project demo • Text, voice, and document translation")

@st.cache_resource(show_spinner="Loading multilingual AI model…")
def load_engine():
    return TranslationEngine(
        model_name=os.getenv("TRANSLATION_MODEL", "facebook/nllb-200-distilled-600M")
    )

with st.sidebar:
    st.header("Model settings")
    st.write("Translation: NLLB-200 distilled 600M")
    st.write("Speech recognition: Whisper (loaded when needed)")
    st.warning("First use downloads model files. A capable computer and internet connection may be required.")
    if st.button("Clear model cache"):
        st.cache_resource.clear()
        st.rerun()

tab_text, tab_voice, tab_doc, tab_about = st.tabs(
    ["✍️ Text", "🎙️ Voice", "📄 Documents", "ℹ️ About & evaluation"]
)

with tab_text:
    left, right = st.columns(2)
    with left:
        src_name = st.selectbox("Source language", list(SUPPORTED_LANGUAGES), index=0, key="text_src")
    with right:
        dst_name = st.selectbox("Target language", list(SUPPORTED_LANGUAGES), index=1, key="text_dst")
    source_text = st.text_area("Enter text", height=180, placeholder="Type or paste text to translate…")
    if st.button("Translate text", type="primary", key="translate_text"):
        if not source_text.strip():
            st.error("Enter some text first.")
        elif src_name == dst_name:
            st.info("Source and target languages are the same.")
            st.text_area("Translation", value=source_text, height=180)
        else:
            try:
                engine = load_engine()
                with st.spinner("Translating…"):
                    translated = engine.translate(source_text, src_name, dst_name)
                st.text_area("Translated text", value=translated, height=180)
                st.download_button("Download translation (.txt)", translated, file_name="translation.txt")
            except Exception as exc:
                st.error(f"Translation failed: {exc}")
                st.info("Check your internet connection, model access, and installed dependencies.")

with tab_voice:
    st.write("Upload an audio recording. Speech is transcribed first, then translated.")
    audio = st.file_uploader("Audio file", type=["wav", "mp3", "m4a", "ogg", "flac"])
    c1, c2 = st.columns(2)
    with c1:
        speech_lang = st.selectbox("Spoken language (Whisper hint)", ["Auto-detect"] + list(SUPPORTED_LANGUAGES), key="speech_lang")
    with c2:
        voice_target = st.selectbox("Translate transcript into", list(SUPPORTED_LANGUAGES), index=1, key="voice_dst")
    if st.button("Transcribe and translate", type="primary", key="voice_translate"):
        if audio is None:
            st.error("Upload an audio file first.")
        else:
            suffix = Path(audio.name).suffix or ".wav"
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(audio.getvalue())
                    audio_path = tmp.name
                try:
                    with st.spinner("Transcribing audio with Whisper…"):
                        lang_hint = None if speech_lang == "Auto-detect" else speech_lang
                        transcript = transcribe_audio(audio_path, language_hint=lang_hint)
                    st.subheader("Recognized speech")
                    st.text_area("Transcript", value=transcript, height=120)
                    source_for_translation = speech_lang if speech_lang != "Auto-detect" else "English"
                    st.caption("For auto-detected speech, choose/confirm the source language below if the result is not English.")
                    actual_src = st.selectbox("Confirm transcript language", list(SUPPORTED_LANGUAGES),
                                               index=list(SUPPORTED_LANGUAGES).index(source_for_translation)
                                               if source_for_translation in SUPPORTED_LANGUAGES else 0,
                                               key="voice_actual_src")
                    if st.button("Translate transcript", key="translate_transcript"):
                        translated = load_engine().translate(transcript, actual_src, voice_target)
                        st.text_area("Translated transcript", value=translated, height=120)
                        st.download_button("Download transcript translation", translated,
                                           file_name="voice_translation.txt")
                finally:
                    os.unlink(audio_path)
            except Exception as exc:
                st.error(f"Voice translation failed: {exc}")
                st.info("Whisper may need to download its model. Try a short, clear audio clip.")

with tab_doc:
    st.write("Supported input formats: TXT, DOCX, and text-based PDF. Scanned PDFs need OCR, which is not included.")
    uploaded_doc = st.file_uploader("Choose document", type=["txt", "docx", "pdf"], key="document")
    d1, d2 = st.columns(2)
    with d1:
        doc_src = st.selectbox("Document source language", list(SUPPORTED_LANGUAGES), key="doc_src")
    with d2:
        doc_dst = st.selectbox("Document target language", list(SUPPORTED_LANGUAGES), index=1, key="doc_dst")
    if st.button("Translate document", type="primary", key="translate_doc"):
        if uploaded_doc is None:
            st.error("Upload a document first.")
        else:
            try:
                extracted = extract_text(uploaded_doc.name, uploaded_doc.getvalue())
                if not extracted.strip():
                    st.error("No text was extracted. If this is a scanned PDF, run OCR first.")
                else:
                    with st.spinner("Translating document text…"):
                        translated_doc = load_engine().translate_long_text(extracted, doc_src, doc_dst)
                    st.subheader("Translated document preview")
                    st.text_area("Translated content", value=translated_doc, height=260)
                    st.download_button("Download translated text (.txt)", translated_doc,
                                       file_name="translated_document.txt")
                    docx_bytes = make_docx(translated_doc)
                    st.download_button("Download translated Word document (.docx)", docx_bytes,
                                       file_name="translated_document.docx")
            except Exception as exc:
                st.error(f"Document translation failed: {exc}")

with tab_about:
    st.subheader("Project abstract")
    st.write(
        "This project implements an AI-assisted multilingual translation system using a pretrained "
        "neural machine translation model. It accepts text, speech recordings, and common text-based "
        "documents. Speech is converted to text using automatic speech recognition, and document "
        "content is extracted before translation. The system provides a simple web interface and "
        "supports quality evaluation with reference translations."
    )
    st.subheader("Important limitations")
    st.markdown(
        "- Supported language pairs depend on the translation model and its language codes.\n"
        "- Automatic speech-language detection is not always reliable; confirm the transcript language.\n"
        "- PDF extraction works for selectable text, not scanned pages without OCR.\n"
        "- Machine translation can make mistakes, especially with idioms, names, and low-resource languages.\n"
        "- Do not upload confidential documents to a demo deployment without a privacy review."
    )
    st.subheader("Suggested evaluation")
    st.markdown(
        "1. Prepare 50–200 source sentences and human reference translations for selected language pairs.\n"
        "2. Record BLEU (and optionally chrF) using SacreBLEU.\n"
        "3. Measure average translation latency and test short/long inputs.\n"
        "4. Have fluent speakers rate adequacy and fluency on a 1–5 scale.\n"
        "5. Compare results by language pair and discuss limitations."
    )

st.divider()
st.caption("Educational prototype. Validate important translations with a fluent speaker.")
