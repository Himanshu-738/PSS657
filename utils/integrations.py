import random

def mock_bureau_check(pan_number: str) -> dict:
    """
    Simulates a credit bureau check using PAN.
    """
    print(f"📡 Running mock bureau check for PAN: {pan_number}")
    # In real world: call Experian/Equifax/CRIF API
    score = random.randint(650, 850)
    return {
        "bureau_score": score,
        "status": "PASS" if score >= 700 else "REVIEW"
    }


def mock_ekyc_check(aadhaar_number: str) -> dict:
    """
    Simulates eKYC check using Aadhaar.
    """
    print(f"📡 Running mock eKYC check for Aadhaar: {aadhaar_number}")
    # In real world: call UIDAI eKYC API
    return {
        "aadhaar_verified": True,
        "name": "Manish Gurjar",
        "dob": "07-June-2006",
        "gender": "Male"
    }
