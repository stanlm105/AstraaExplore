import re

def validate_name(name: str) -> str:
    """
    Validate and sanitize a user-supplied name for PDF personalization.
    Only allows characters safe for filenames: letters, numbers, spaces, hyphens, underscores, apostrophes, and periods.

    Args:
        name (str): The name to validate.

    Returns:
        str: The validated and sanitized name.

    Raises:
        ValueError: If the name is invalid.
    """
    if not isinstance(name, str):
        raise ValueError("Name must be a string.")
    name = name.strip()
    if len(name) == 0 or len(name) > 50:
        raise ValueError("Name must be 1-50 characters long.")
    # Only allow filename-safe characters
    if not re.match(r"^[A-Za-z0-9 ._\-']+$", name):
        raise ValueError("Name contains invalid characters. Allowed: letters, numbers, spaces, hyphens, underscores, apostrophes, and periods.")
    return name