import random
from utils.input_utils import safe_input

# Store OTPs in-memory (simulate)
otp_store = {}

def generate_otp(user_id: str) -> str:
    """
    Generate a 6-digit OTP for the given user_id.
    """
    otp = str(random.randint(100000, 999999))
    otp_store[user_id] = otp
    print(f"📩 [Simulated] OTP sent to user: {otp}")  # Simulate sending
    return otp

def validate_otp(user_id: str, entered_otp: str, lang: str = "en") -> bool:
    """
    Validate the entered OTP.
    """
    correct_otp = otp_store.get(user_id)
    if entered_otp == correct_otp:
        return True
    return False

def prompt_for_otp(user_id: str, lang: str = "en", collected: dict = None) -> str:
    """
    Prompt user to enter OTP safely with exit support.
    """
    if collected is None:
        collected = {}

    prompt_text = (
        "📩 Please enter the OTP sent to your phone/email:\n> "
        if lang == "en"
        else "📩 कृपया अपने फोन/ईमेल पर भेजा गया OTP दर्ज करें:\n> "
    )

    entered = safe_input(prompt_text, user_id, collected, lang=lang)
    return entered