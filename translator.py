import re
from functools import lru_cache
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# NLLB-200 language tags. Add only language tags supported by the chosen model.
SUPPORTED_LANGUAGES = {
    "English": "eng_Latn",
    "Telugu": "tel_Telu",
    "Hindi": "hin_Deva",
    "Tamil": "tam_Taml",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym",
    "Bengali": "ben_Beng",
    "Marathi": "mar_Deva",
    "Gujarati": "guj_Gujr",
    "Punjabi": "pan_Guru",
    "Urdu": "urd_Arab",
    "French": "fra_Latn",
    "Spanish": "spa_Latn",
    "German": "deu_Latn",
    "Portuguese": "por_Latn",
    "Arabic": "arb_Arab",
    "Chinese (Simplified)": "zho_Hans",
    "Japanese": "jpn_Jpan",
    "Korean": "kor_Hang",
    "Russian": "rus_Cyrl",
}

class TranslationEngine:
    def __init__(self, model_name="facebook/nllb-200-distilled-600M", device=None):
        import torch
        self.torch = torch
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model.to(device)
        self.model.eval()

    def translate(self, text, source_language, target_language, max_new_tokens=512):
        if not text or not text.strip():
            return ""
        if source_language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported source language: {source_language}")
        if target_language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported target language: {target_language}")
        if source_language == target_language:
            return text

        src_code = SUPPORTED_LANGUAGES[source_language]
        tgt_code = SUPPORTED_LANGUAGES[target_language]
        self.tokenizer.src_lang = src_code
        encoded = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
        encoded = {k: v.to(self.device) for k, v in encoded.items()}
        forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(tgt_code)
        with self.torch.inference_mode():
            generated = self.model.generate(
                **encoded,
                forced_bos_token_id=forced_bos_token_id,
                max_new_tokens=max_new_tokens,
                num_beams=4,
            )
        return self.tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

    def translate_long_text(self, text, source_language, target_language, max_chars=1200):
        # Paragraph-based chunking keeps long documents within practical model input limits.
        paragraphs = re.split(r"\n\s*\n", text.strip())
        output = []
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue
            sentences = re.split(r"(?<=[.!?।؟])\s+", paragraph.strip())
            chunks, current = [], ""
            for sentence in sentences:
                if len(current) + len(sentence) + 1 <= max_chars:
                    current = f"{current} {sentence}".strip()
                else:
                    if current:
                        chunks.append(current)
                    current = sentence
            if current:
                chunks.append(current)
            translated = [self.translate(chunk, source_language, target_language)
                          for chunk in chunks]
            output.append(" ".join(translated))
        return "\n\n".join(output)
