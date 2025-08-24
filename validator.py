import json
import sys
import os

REQUIRED_FIELDS = ["name", "profession", "quote", "github"]

TEMPLATE_VALUES = {
    "name": "Your Name",
    "profession": "Your Profession",
    "quote": "\"Your favourite quote\"</br> - Said By Me",
    "github": "https://github.com"
}

def is_template_entry(card):
    """Check if the entry is a template or not"""
    return all(card.get(k) == v for k, v in TEMPLATE_VALUES.items() if k in card)

def validate_json(file_path):
    errors = []

    if not os.path.exists(file_path):
        errors.append(f"❌ File not found: {file_path}")
        return errors

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"❌ JSON Syntax Error: {str(e)}")
        return errors

    if "cardDetails" not in data:
        errors.append("❌ Missing 'cardDetails' key at root level.")
        return errors

    seen = set()  

    for idx, card in enumerate(data["cardDetails"], start=1):
        # Template entries ko skip karo
        if is_template_entry(card):
            continue

        # Required field check
        for field in REQUIRED_FIELDS:
            if field not in card or not str(card[field]).strip():
                errors.append(f"❌ Entry {idx} missing required field: {field}")

               # Duplicate check (by Name + GitHub link)
        fingerprint = (
            card.get("name", "").strip().lower(),
            card.get("github", "").strip().lower()
        )
        if fingerprint in seen:
            errors.append(
                f"❌ Duplicate entry found at index {idx} → Name: '{card.get('name')}', GitHub: {card.get('github')}"
            )
        else:
            seen.add(fingerprint)

    return errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python validator.py <path_to_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    errors = validate_json(file_path)

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    else:
        print("✅ JSON Validation Passed! All required fields and no duplicates.")
        sys.exit(0)