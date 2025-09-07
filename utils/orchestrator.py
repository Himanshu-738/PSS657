import datetime
import requests
from db.mongo_client import transactions
# mapping table example
MAPPING = {
    "res_status_id": {
        "Owned": 1,
        "Rented": 2,
        "Employer Provided": 3
    }
}

def apply_master_mapping(data):
    # Apply mappings for known fields. Use mapping keys from config.
    mapped = data.copy()
    if "res_status" in data:
        mapped["res_status_id"] = MAPPING["res_status_id"].get(data["res_status"], None)
    return mapped

def prepare_payload(data):
    # Build unified payload expected by backend/core
    mapped = apply_master_mapping(data)
    payload = {
        "applicant": {
            "name": mapped.get("full_name") or mapped.get("name"),
            "dob": mapped.get("dob"),
            "gender": mapped.get("gender"),
            "mobile": mapped.get("mobile"),
            "email": mapped.get("email")
        },
        "addresses": {
            "current": mapped.get("current_address"),
            "permanent": mapped.get("permanent_address")
        },
        "income": {
            "monthly_income": mapped.get("monthly_income")
        },
        "bank": {
            "bank_name": mapped.get("bank_name"),
            "account_no": mapped.get("account_no"),
            "ifsc": mapped.get("ifsc")
        },
        "meta": {
            "res_status_id": mapped.get("res_status_id")
        },
        "raw": mapped
    }
    return payload

def push_to_core(payload):
    # Simulated push. Replace with requests.post to real core endpoint.
    print("📤 Pushing payload to core system (simulated)...")
    # Simulated response
    response = {"status": "success", "core_application_id": "CORE123456"}
    return response

def log_transaction(user_id, payload, response):
    doc = {
        "user_id": user_id,
        "payload": payload,
        "core_response": response,
        "timestamp": datetime.datetime.utcnow()
    }
    transactions.insert_one(doc)
    return doc
