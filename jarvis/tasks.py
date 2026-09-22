from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid4

@dataclass(slots=True)
class Task:
    id: str
    title: str
    completed: bool = False
    priority: str = "normal"
    due_at: str | None = None
    recurrence: str | None = None

class TaskStore:
    def __init__(self, path: str | Path = ".jarvis_tasks.json") -> None:
        self.path = Path(path)
        self.tasks = self._load()
    def _load(self) -> list[Task]:
        try: return [Task(**item) for item in json.loads(self.path.read_text(encoding="utf-8"))]
        except (FileNotFoundError, json.JSONDecodeError, TypeError): return []
    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True); self.path.write_text(json.dumps([asdict(t) for t in self.tasks], indent=2), encoding="utf-8")
    def create(self, title: str, *, due_at: datetime | None = None, recurrence: str | None = None, priority: str = "normal") -> Task:
        if not title.strip(): raise ValueError("Task title is required")
        task = Task(str(uuid4()), title.strip(), priority=priority, due_at=due_at.isoformat() if due_at else None, recurrence=recurrence)
        self.tasks.append(task); self._save(); return task
    def list(self, include_completed: bool = False) -> list[Task]: return [t for t in self.tasks if include_completed or not t.completed]
    def complete(self, task_id: str) -> Task:
        task = self._find(task_id); task.completed = True; self._save(); return task
    def _find(self, task_id: str) -> Task:
        for task in self.tasks:
            if task.id == task_id: return task
        raise ValueError("Task not found")
