import json
import sys
import os

REQUIRED_FIELDS = ["name", "profession", "quote", "github"]

# Template values to skip
TEMPLATE_VALUES = {
    "name": "Your Name",
    "profession": "Your Profession",
    "quote": "\"Your favourite quote\"</br> - Said By Me",
    "github": "https://github.com"
}

def is_template_entry(card):
    """Check kare ki entry template hai ya nahi"""
    return all(card.get(k) == v for k, v in TEMPLATE_VALUES.items() if k in card)

def validate_json(file_path):
    errors = []
    valid_names = []

    if not os.path.exists(file_path):
        errors.append(f"❌ File not found: {file_path}")
        return errors, valid_names

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"❌ JSON Syntax Error: {str(e)}")
        return errors, valid_names

    if "cardDetails" not in data:
        errors.append("❌ Missing 'cardDetails' key at root level.")
        return errors, valid_names

    seen = set()   # track duplicates

    for idx, card in enumerate(data["cardDetails"], start=1):
        # Skip template entries
        if is_template_entry(card):
            continue

        name = card.get("name", f"(unknown at index {idx})")
        has_error = False

        # Required field check
        for field in REQUIRED_FIELDS:
            if field not in card or not str(card[field]).strip():
                errors.append(f"❌ Error in Entry {idx} ('{name}') → missing required field: {field}")
                has_error = True

        # Duplicate check (by Name + GitHub link)
        fingerprint = (
            card.get("name", "").strip().lower(),
            card.get("github", "").strip().lower()
        )
        if fingerprint in seen:
            errors.append(
                f"❌ Error in Entry {idx} ('{name}') → Duplicate entry (GitHub: {card.get('github')})"
            )
            has_error = True
        else:
            seen.add(fingerprint)

        # Add to valid list if no errors
        if not has_error:
            valid_names.append(name)

    return errors, valid_names


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python validator.py <path_to_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    errors, valid_names = validate_json(file_path)

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    else:
        print("✅ JSON Validation Passed!")
        print("👥 Valid Entries:")
        for n in valid_names:
            print(f"   - {n}")
        sys.exit(0)
