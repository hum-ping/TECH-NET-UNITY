from __future__ import annotations

import json
from pathlib import Path


class Memory:
    """Small local JSON memory; never stores credentials or secrets."""

    def __init__(self, path: str = ".jarvis_memory.json"):
        self.path = Path(path)
        self.data = self._load()

    def _load(self) -> dict:
        try:
            value = json.loads(self.path.read_text())
            return value if isinstance(value, dict) else {"notes": []}
        except (FileNotFoundError, json.JSONDecodeError):
            return {"notes": []}

    def add_note(self, note: str) -> None:
        clean = note.strip()
        if not clean:
            return
        self.data.setdefault("notes", []).append(clean)
        self.data["notes"] = self.data["notes"][-100:]
        self.path.write_text(json.dumps(self.data, indent=2))

    def recent(self, limit: int = 10) -> list[str]:
        return self.data.get("notes", [])[-limit:]
