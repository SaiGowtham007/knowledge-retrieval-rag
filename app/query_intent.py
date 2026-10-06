import re


CURRENT_KEYWORDS = [
    "current",
    "latest",
    "active",
    "production",
    "effective",
    "currently"
]


def detect_document_status(question: str) -> str | None:
    question_lower = question.lower()

    for keyword in CURRENT_KEYWORDS:
        if keyword in question_lower:
            return "CURRENT"

    return None


def detect_version(question: str) -> str | None:
    match = re.search(r"\bv\d+(?:\.\d+)+\b", question.lower())

    if match:
        return match.group(0)

    return None