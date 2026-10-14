import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = PROJECT_ROOT / "src" / "validator.py"

spec = importlib.util.spec_from_file_location("validator", VALIDATOR_PATH)
validator_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator_module)

validate_json = validator_module.validate_json


def test_valid_data():
    result = validate_json({"name": "Alice", "age": 23})
    assert result["valid"] is True
    assert result["errors"] == []


def test_missing_required_field():
    result = validate_json({"name": "Alice"})
    assert result["valid"] is False
    assert any("age" in error["message"] for error in result["errors"])


def test_wrong_field_type():
    result = validate_json({"name": "Alice", "age": "23"})
    assert result["valid"] is False


def test_additional_property():
    result = validate_json({"name": "Alice", "age": 23, "city": "Paris"})
    assert result["valid"] is False


def test_error_type_missing_required_field():
    result = validate_json({"name": "Alice"})
    assert result["errors"][0]["type"] == "missing_required_field"


def test_error_type_wrong_type():
    result = validate_json({"name": "Alice", "age": "23"})
    assert result["errors"][0]["type"] == "wrong_type"


def test_error_type_additional_property():
    result = validate_json({"name": "Alice", "age": 23, "city": "Paris"})
    assert result["errors"][0]["type"] == "additional_property"


def test_error_path():
    result = validate_json({"name": "Alice", "age": "23"})
    assert result["errors"][0]["path"] == "/age"
