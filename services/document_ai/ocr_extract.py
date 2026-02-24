def extract_from_aadhaar(file_path):
    """
    Placeholder OCR extraction.
    Later integrate real OCR (Tesseract / API).
    """
    return {
        "name": "Sample User",
        "aadhaar_number": "XXXX-XXXX-1234",
        "confidence": 0.75
    }


def extract_from_land_document(file_path):
    """
    Extract land size & ownership details.
    """
    return {
        "land_size": "2 acres",
        "owner_name": "Sample User",
        "confidence": 0.72
    }


def extract_from_bank_statement(file_path):
    """
    Extract income signals from statement.
    """
    return {
        "monthly_income_estimate": 18000,
        "transaction_stability": "moderate",
        "confidence": 0.70
    }