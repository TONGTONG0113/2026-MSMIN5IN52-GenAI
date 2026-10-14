import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


SCHEMA_DIR = Path(__file__).parent / "schemas"


def load_schema(schema_name: str = "schema_01.json") -> dict:
    """Charge un schéma JSON depuis le dossier schemas."""
    schema_path = SCHEMA_DIR / schema_name

    with schema_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def classify_error(error) -> str:
    """Classe une erreur de validation JSON."""
    if error.validator == "required":
        return "missing_required_field"
    if error.validator == "type":
        return "wrong_type"
    if error.validator == "additionalProperties":
        return "additional_property"
    if error.validator == "minimum":
        return "value_below_minimum"
    if error.validator == "format":
        return "invalid_format"
    return "constraint_violation"


def validate_json(data: Any, schema_name: str = "schema_01.json") -> dict:
    """Valide des données JSON et retourne les erreurs classées."""
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema)

    errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (
            list(map(str, error.absolute_path)),
            error.message,
        ),
    )

    return {
        "valid": len(errors) == 0,
        "errors": [
            {
                "path": "/" + "/".join(str(part) for part in error.absolute_path),
                "message": error.message,
                "type": classify_error(error),
            }
            for error in errors
        ],
    }
