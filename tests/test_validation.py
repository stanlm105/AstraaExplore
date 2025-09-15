import pytest
from utils.validation import validate_name

@pytest.mark.parametrize("name", [
    "Alice",
    "Bob Smith",
    "O'Connor",
    "Jane-Doe_42",
    "A" * 50,
    "John.Doe"
])
def test_validate_name_valid(name):
    assert validate_name(name) == name.strip()

@pytest.mark.parametrize("name", [
    "",
    "A" * 51,
    "Name/With/Slash",
    "Name\\With\\Backslash",
    "Name:With:Colon",
    "Name*With*Star",
    None,
    123
])
def test_validate_name_invalid(name):
    with pytest.raises(ValueError):
        validate_name(name)