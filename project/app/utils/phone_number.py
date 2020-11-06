import re

# Regex string to reuse at other place (ex: at frontend js)
PHONE_REGEX = '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'


def export_phone_numbers(raw_text: str) -> str:
    expored_phone_numbers = re.findall(
        rf'{PHONE_REGEX}', raw_text, re.MULTILINE
    )
    return ",".join(expored_phone_numbers)
