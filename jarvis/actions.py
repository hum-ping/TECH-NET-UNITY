from __future__ import annotations

from .computer import ComputerController


class ActionRouter:
    """Translate human commands into a small, explicit action set."""

    def __init__(self, computer: ComputerController | None = None):
        self.computer = computer or ComputerController()

    def handle(self, text: str, confirm: bool = False) -> str:
        raw = text.strip()
        lower = raw.lower()
        if not raw:
            return "Please give me a command."
        if lower in {"stop", "emergency stop", "shutdown jarvis"}:
            return "STOP_REQUESTED"
        if lower in {"status", "system status"}:
            return str(self.computer.system_info())
        if lower.startswith("open "):
            target = raw[5:].strip()
            return self.computer.open_target(target, confirmed=confirm)
        return "I can safely handle: status, open <allowlisted app/url>, and emergency stop."
