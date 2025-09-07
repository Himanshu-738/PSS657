import re
from dateutil import parser
import phonenumbers
import validators

def validate_phone(value, country="IN"):
    try:
        p = phonenumbers.parse(value, country)
        return phonenumbers.is_valid_number(p)
    except Exception:
        # fallback: 10-digit numeric
        return bool(re.fullmatch(r"\d{10}", re.sub(r"\D", "", value)))

def validate_email(value):
    try:
        return validators.email(value)
    except Exception:
        return False

def validate_date(value):
    try:
        dt = parser.parse(value, dayfirst=True)
        return dt.date().isoformat()
    except Exception:
        return None

def validate_number(value):
    try:
        # accept integers or floats (strip commas)
        v = str(value).replace(",", "")
        if v == "":
            return None
        return float(v)
    except Exception:
        return None

def validate_regex(value, pattern):
    return bool(re.fullmatch(pattern, value))
