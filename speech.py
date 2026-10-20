from transformers import pipeline

def transcribe_audio(audio_path, language_hint=None, model_name="openai/whisper-small"):
    """
    Transcribe an audio file using Whisper.
    language_hint is a display language such as 'English' or 'Hindi'; Whisper expects
    language names, so this function passes the supplied name as a hint.
    """
    asr = pipeline(
        "automatic-speech-recognition",
        model=model_name,
        chunk_length_s=30,
        return_timestamps=False,
    )
    kwargs = {"task": "transcribe"}
    if language_hint:
        kwargs["language"] = language_hint
    result = asr(audio_path, generate_kwargs=kwargs)
    return result["text"].strip()
