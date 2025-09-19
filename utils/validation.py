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

def sanitize_room(room: str) -> str:
    """Sanitize room name: allow letters, numbers, _, -, max 25 chars."""
    room = room.strip()
    room = re.sub(r'[^A-Za-z0-9_\-]', '', room)
    return room[:25]

def sanitize_country(country: str) -> str:
    """Sanitize country: uppercase, only letters, max 2 chars."""
    country = country.strip().upper()
    return re.sub(r'[^A-Z]', '', country)[:2]

def sanitize_zipcode(zipcode: str) -> str:
    """Sanitize zipcode: allow letters/numbers, max 10 chars."""
    zipcode = zipcode.strip()
    return re.sub(r'[^A-Za-z0-9]', '', zipcode)[:10]

def sanitize_passphrase(passphrase: str) -> str:
    """Sanitize passphrase: trim, max 50 chars."""
    return passphrase.strip()[:50]

def sanitize_bortle_score(bortle: str) -> str:
    """Allow only digits 1-9, max 1 char."""
    bortle = bortle.strip()
    match = re.match(r'^[1-9]$', bortle)
    return bortle if match else ""

def sanitize_seen_list(seen_list: str) -> str:
    """Allow only comma-separated numbers, sorted, no duplicates."""
    nums = set()
    for part in seen_list.split(","):
        part = part.strip()
        if part.isdigit():
            nums.add(int(part))
    return ",".join(str(num) for num in sorted(nums))
