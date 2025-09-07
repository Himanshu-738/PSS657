from utils.orchestrator import log_transaction
import sys

def safe_input(prompt: str, user_id: str, collected: dict, *, lang: str = "en") -> str:
    """
    Safe wrapper around input() that supports exit/quit commands.
    Logs incomplete transaction before exiting.
    'lang' is keyword-only to avoid duplicate assignment issues.
    """
    try:
        user_input = input(prompt)

        if user_input.strip().lower() in ["exit", "quit", "बाहर"]:
            msg = "👋 Exiting the bot. Thank you!" if lang == "en" else "👋 बॉट से बाहर निकला जा रहा है। धन्यवाद!"
            print(msg)

            # Log incomplete session
            log_transaction(user_id, collected, {"status": "incomplete", "reason": "user_exit"})
            sys.exit(0)

        return user_input.strip()

    except KeyboardInterrupt:
        msg = "\n👋 Exiting the bot (KeyboardInterrupt). Thank you!" if lang == "en" else "\n👋 बॉट से बाहर निकला जा रहा है (कीबोर्ड इंटरप्ट)। धन्यवाद!"
        print(msg)
        log_transaction(user_id, collected, {"status": "incomplete", "reason": "keyboard_interrupt"})
        sys.exit(0)
