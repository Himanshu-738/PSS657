from utils.translator import translate_text
from utils.input_utils import safe_input
from utils.ocr import fake_ocr
from utils.integrations import mock_bureau_check, mock_ekyc_check
from utils.photo import mock_liveliness_check


def run_flow(user_id: str, lang: str = "en"):
    responses = {}

    # Step 0 – Document Upload
    q_text = "📌 Please provide path to your ID document (e.g., sample_id.png):"
    doc_path = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )
    ocr_result = fake_ocr(doc_path)
    responses.update(ocr_result)

    print("\n✅ Extracted details from your document:")
    for k, v in ocr_result.items():
        print(f"{k}: {v}")

    # Step 1 – Personal Details
    q_text = "Can I have your full name as per your official documents? (auto-filled): " + responses.get("full_name", "")
    responses["full_name"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    ) or responses["full_name"]

    q_text = "What is your date of birth? (DD-MM-YYYY) (auto-filled): " + responses.get("dob", "")
    responses["dob"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    ) or responses["dob"]

    q_text = "Gender?"
    responses["gender"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    q_text = "Which mobile number should we use to contact you? (10 digits)"
    responses["mobile"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    q_text = "And your email address?"
    responses["email"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    # Step 2 – Other Details
    q_text = "What’s your current residential address?"
    responses["current_address"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    q_text = "Is this owned, rented, or provided by your employer?"
    responses["residence_type"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    q_text = "How long have you been staying here?"
    responses["residence_duration"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    q_text = "Do you have a different permanent address?"
    responses["permanent_address"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    q_text = "What’s your monthly net income after deductions?"
    responses["income"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    q_text = "Which bank account should we use for loan disbursement?"
    responses["bank_name"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    q_text = "Can you confirm the account number and IFSC code?"
    responses["account_details"] = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    # Step 3 – API checks
    if "id_number" in responses:
        responses.update(mock_bureau_check(responses["id_number"]))

    aadhaar_num = safe_input(
        "Please enter your Aadhaar number:\n> ",
        user_id,
        responses,
        lang=lang
    )
    responses.update(mock_ekyc_check(aadhaar_num))

     # Step 4 – Photo Capture with Liveliness
    q_text = "Please provide a path to your selfie image for liveliness check:"
    selfie_path = safe_input(
        translate_text(q_text, lang) + "\n> ",
        user_id,
        responses,
        lang=lang
    )

    # Pass user_id and collected dict to upgraded function
    responses.update(mock_liveliness_check(selfie_path, user_id, responses, lang=lang))

    return responses
