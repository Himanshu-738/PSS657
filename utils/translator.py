from googletrans import Translator

translator = Translator()

def translate_text(text: str, target: str = "en") -> str:
    """
    Translate text into target language.
    target: "en" for English, "hi" for Hindi
    """
    try:
        return translator.translate(text, dest=target).text
    except Exception as e:
        print(f"⚠️ Translation failed: {e}")
        return text

def detect_and_translate(text: str, target: str = "en") -> str:
    """
    Detect source language and translate into target.
    """
    try:
        result = translator.translate(text, dest=target)
        return result.text
    except Exception as e:
        print(f"⚠️ Detection/translation failed: {e}")
        return text
