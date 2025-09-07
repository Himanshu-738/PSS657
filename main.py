import uuid
from agents.flow import run_flow
from utils.otp import generate_otp, validate_otp, prompt_for_otp
from utils.orchestrator import prepare_payload, push_to_core, log_transaction
from utils.input_utils import safe_input

if __name__ == "__main__":
    user_id = str(uuid.uuid4())
    collected = {}  # responses storage

    print("👋 Welcome to Loan Onboarding Agent!")
    print("🌐 Please select your language / कृपया अपनी भाषा चुनें:")
    print("1. English")
    print("2. हिंदी (Hindi)")

    # Correct call to safe_input
    choice = safe_input("> ", user_id, collected, lang="en")
    lang = "hi" if choice.strip() == "2" else "en"

    # OTP Verification
    otp = generate_otp(user_id)
    entered = prompt_for_otp(user_id, lang)

    if not validate_otp(user_id, entered, lang):
        msg = "❌ OTP invalid. Exiting." if lang == "en" else "❌ OTP अमान्य है। बाहर निकला जा रहा है।"
        print(msg)
        exit()

    print("✅ OTP verified successfully!\n" if lang == "en" else "✅ OTP सफलतापूर्वक सत्यापित!\n")

    # Run Onboarding Flow
    collected = run_flow(user_id, lang=lang)

    # Prepare payload and push to core
    payload = prepare_payload(collected)
    core_resp = push_to_core(payload)
    tx_doc = log_transaction(user_id, payload, core_resp)

    print("\n🎉 Final Payload submitted (simulated)." if lang=="en" else "\n🎉 अंतिम डेटा (पेलोड) सबमिट किया गया।")
    print(core_resp)
    print("\n🗄️ Transaction logged with ID (Mongo):", tx_doc.get("_id"))
    