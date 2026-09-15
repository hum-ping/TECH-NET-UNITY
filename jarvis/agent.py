from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from threading import Event

from .actions import ActionRouter
from .computer import ComputerController
from .config import settings
from .routines import DEFAULT_ROUTINE, due_tasks


class JarvisAgent:
    """Always-running local agent with routines, commands, and an emergency stop."""

    def __init__(self, state_file: str = ".jarvis_state.json"):
        self.computer = ComputerController()
        self.router = ActionRouter(self.computer)
        self.state_file = Path(state_file)
        self.stop_event = Event()
        self.last_run = self._load_state()

    def _load_state(self) -> dict:
        try:
            value = json.loads(self.state_file.read_text())
            return value if isinstance(value, dict) else {"routine_keys": []}
        except (FileNotFoundError, json.JSONDecodeError):
            return {"routine_keys": []}

    def _save_state(self) -> None:
        self.state_file.write_text(json.dumps(self.last_run, indent=2))

    def emergency_stop(self) -> None:
        self.stop_event.set()
        print("JARVIS emergency stop engaged.")

    def run_task(self, task) -> str:
        messages = {
            "briefing": "Good morning. JARVIS is online. Review priorities and market status before trading.",
            "notify_midday": "Midday check: review priorities, open positions, and risk limits.",
            "daily_review": "End-of-day review: summarize work, journal trades, and prepare tomorrow's priorities.",
            "open_work_apps": "Work-app launch is available only for explicitly allowlisted applications.",
        }
        return self.computer.notify(messages.get(task.command, f"Unknown routine: {task.command}"))

    def tick(self, now: datetime | None = None) -> list[str]:
        now = now or datetime.now()
        key_prefix = now.strftime("%Y-%m-%d")
        results = []
        for task in due_tasks(now, DEFAULT_ROUTINE):
            key = f"{key_prefix}:{task.time}:{task.command}"
            if key in self.last_run["routine_keys"]:
                continue
            result = self.run_task(task)
            results.append(result)
            self.last_run["routine_keys"].append(key)
        self.last_run["routine_keys"] = self.last_run["routine_keys"][-100:]
        self._save_state()
        return results

    def run_command(self, text: str, confirmed: bool = False) -> str:
        result = self.router.handle(text, confirm=confirmed)
        if result == "STOP_REQUESTED":
            self.emergency_stop()
            return "JARVIS stopped safely."
        return result

    def run_forever(self, interval_seconds: int = 20) -> None:
        self.computer.notify(f"{settings.name} agent started. Emergency stop: Ctrl+C.")
        while not self.stop_event.is_set():
            for result in self.tick():
                if result:
                    print(result)
            self.stop_event.wait(interval_seconds)


if __name__ == "__main__":
    try:
        JarvisAgent().run_forever()
    except KeyboardInterrupt:
        print("JARVIS stopped safely.")
