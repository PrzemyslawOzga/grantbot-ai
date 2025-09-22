from datetime import datetime, timezone
import uuid


def current_utc_time():
    """Return current UTC time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def new_uuid():
    """Return a new UUID string."""
    return str(uuid.uuid4())
