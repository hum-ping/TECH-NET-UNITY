from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from threading import Event

from .computer import ComputerController
from .routines import DEFAULT_ROUTINE, due_tasks


class JarvisAgent:
    """Always-running local agent with safe, explicit actions only."""

    def __init__(self, state_file: str = ".jarvis_state.json"):
        self.computer = ComputerController()
        self.state_file = Path(state_file)
        self.stop_event = Event()
        self.last_run = self._load_state()

    def _load_state(self) -> dict:
        try:
            return json.loads(self.state_file.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return {"routine_keys": []}

    def _save_state(self) -> None:
        self.state_file.write_text(json.dumps(self.last_run, indent=2))

    def emergency_stop(self) -> None:
        self.stop_event.set()

    def run_task(self, task) -> str:
        if task.command == "briefing":
            return self.computer.notify("Good morning. JARVIS is online. Review your priorities and market status before trading.")
        if task.command == "notify_midday":
            return self.computer.notify("Midday check: review priorities, open positions, and risk limits.")
        if task.command == "daily_review":
            return self.computer.notify("End-of-day review: summarize work, journal trades, and prepare tomorrow's priorities.")
        if task.command == "open_work_apps":
            return self.computer.notify("Work-app launch is configured as a safe extension point; add explicit apps to the allowlist before enabling it.")
        return f"Unknown routine: {task.command}"

    def tick(self, now: datetime | None = None) -> list[str]:
        now = now or datetime.now()
        key_prefix = now.strftime("%Y-%m-%d")
        results = []
        for task in due_tasks(now, DEFAULT_ROUTINE):
            key = f"{key_prefix}:{task.time}:{task.command}"
            if key in self.last_run["routine_keys"]:
                continue
            results.append(self.run_task(task))
            self.last_run["routine_keys"].append(key)
        self.last_run["routine_keys"] = self.last_run["routine_keys"][-100:]
        self._save_state()
        return results

    def run_forever(self, interval_seconds: int = 20) -> None:
        self.computer.notify("JARVIS agent started. Emergency stop: Ctrl+C.")
        while not self.stop_event.is_set():
            for result in self.tick():
                print(result)
            self.stop_event.wait(interval_seconds)


if __name__ == "__main__":
    try:
        JarvisAgent().run_forever()
    except KeyboardInterrupt:
        print("JARVIS stopped safely.")
