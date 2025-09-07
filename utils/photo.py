import random
from utils.input_utils import safe_input

def mock_liveliness_check(photo_path: str, user_id: str, collected: dict, lang: str = "en") -> dict:
    """
    Simulate photo capture + liveliness check.
    - Asks user to confirm they are holding the camera/selfie device.
    - Randomly fails ~10% of the time to simulate liveliness detection.
    Returns a dictionary with 'photo_verified' flag.
    """
    print(f"📸 Simulated photo capture for file: {photo_path}")

    # Step 1: Ask user to confirm holding camera
    prompt_text = (
        "Please confirm you are holding the camera in front of you (yes/no):\n> "
        if lang == "en"
        else "कृपया पुष्टि करें कि आप कैमरा सामने रख रहे हैं (हाँ/ना):\n> "
    )
    confirm = safe_input(prompt_text, user_id, collected, lang=lang).lower()

    # Step 2: Randomly fail 10% of the time
    failure_chance = random.randint(1, 10)
    if confirm in ["yes", "हाँ"] and failure_chance != 1:
        verified = True
        msg = "✅ Photo verified successfully!" if lang == "en" else "✅ फोटो सफलतापूर्वक सत्यापित!"
    else:
        verified = False
        msg = "❌ Photo verification failed." if lang == "en" else "❌ फोटो सत्यापन असफल।"

    print(msg)
    return {"photo_path": photo_path, "photo_verified": verified}