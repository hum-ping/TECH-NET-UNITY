"""Local, categorized memory with basic secret-resistance."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Literal

MemoryKind = Literal["conversation", "preferences", "facts", "project", "trading", "system"]
_SECRET = re.compile(r"(?:api[_ -]?key|password|secret|token|authorization)\s*[:=]", re.I)

class Memory:
    """Small persistent JSON memory. Credentials are rejected rather than persisted."""
    def __init__(self, path: str | Path = ".jarvis_memory.json"):
        self.path = Path(path)
        self.data = self._load()

    def _load(self) -> dict:
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {"notes": [], "entries": []}
        except (FileNotFoundError, json.JSONDecodeError):
            return {"notes": [], "entries": []}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def remember(self, text: str, kind: MemoryKind = "facts") -> bool:
        clean = text.strip()
        if not clean or _SECRET.search(clean):
            return False
        entry = {"kind": kind, "text": clean}
        self.data.setdefault("entries", []).append(entry)
        self.data["entries"] = self.data["entries"][-300:]
        self._save()
        return True

    def add_note(self, note: str) -> None:
        if self.remember(note, "conversation"):
            self.data.setdefault("notes", []).append(note.strip())
            self.data["notes"] = self.data["notes"][-100:]
            self._save()

    def recall(self, query: str = "", *, kind: MemoryKind | None = None, limit: int = 10) -> list[str]:
        terms = set(query.lower().split())
        entries = self.data.get("entries", [])
        found = [e["text"] for e in entries if (kind is None or e.get("kind") == kind) and (not terms or terms & set(e.get("text", "").lower().split()))]
        return found[-max(0, limit):]

    def forget(self, text: str) -> int:
        before = self.data.get("entries", [])
        self.data["entries"] = [entry for entry in before if entry.get("text") != text]
        self._save()
        return len(before) - len(self.data["entries"])

    def recent(self, limit: int = 10) -> list[str]:
        return self.recall(limit=limit)
