def fake_ocr(file_path):
    # Simulated OCR. In real mode, replace with actual OCR API call.
    print(f"📄 (simulated) Processing file: {file_path}")
    # Return keys that match question ids expected in config returns
    return {
        "full_name": "Rohan Mehta",
        "dob": "15-08-1992",
        "id_number": "ABCDE1234F"
    }
