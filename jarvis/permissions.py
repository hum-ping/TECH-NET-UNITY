"""Compatibility adapter for legacy computer action checks."""
from dataclasses import dataclass
from .core import PermissionDenied, PermissionLevel, PermissionManager

@dataclass(frozen=True)
class ActionPolicy:
    allowed: frozenset[str] = frozenset({"open_app", "open_url", "read_clipboard", "write_clipboard", "type_text", "hotkey", "take_screenshot", "notify"})
    confirmation_required: frozenset[str] = frozenset({"type_text", "hotkey", "write_clipboard"})

class PermissionGate:
    def __init__(self, policy: ActionPolicy | None = None):
        self.policy = policy or ActionPolicy()
        self.manager = PermissionManager()

    def check(self, action: str, confirmed: bool = False) -> None:
        if action not in self.policy.allowed:
            raise PermissionDenied(f"Action not allowlisted: {action}")
        level = PermissionLevel.USER_CONFIRMATION if action in self.policy.confirmation_required else PermissionLevel.LOW_RISK
        self.manager.authorize(level, confirmed=confirmed, emergency_stopped=False)
