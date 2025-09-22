import json
from app.config import HISTORY_FILE
from app.utils.helpers import current_utc_time, new_uuid


class HistoryStorage:
    """Store and manage history of generated sections in a JSON file."""

    def __init__(self, path=HISTORY_FILE):
        self.path = path
        self._ensure_file()

    def _ensure_file(self):
        """Ensure the JSON file exists."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]")

    def add(self, company_id, section_type, request_id=None):
        """Add a new history entry."""
        entry = {
            "request_id": request_id or new_uuid(),
            "company_id": company_id,
            "section_type": section_type,
            "created_at": current_utc_time(),
        }
        all_entries = self._read_all()
        all_entries.append(entry)
        self.path.write_text(
            json.dumps(all_entries, ensure_ascii=False, indent=2)
        )
        print(f"Saved history entry: {entry['request_id']}")
        return entry

    def _read_all(self):
        """Read all history entries from the file."""
        try:
            return json.loads(self.path.read_text())
        except Exception:
            return []

    def list_for_company(self, company_id):
        """Return all history entries for a specific company."""
        all_entries = self._read_all()
        company_entries = []
        for entry in all_entries:
            if entry.get("company_id") == company_id:
                company_entries.append(entry)
        return company_entries
