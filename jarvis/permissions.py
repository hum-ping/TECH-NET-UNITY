from dataclasses import dataclass

@dataclass(frozen=True)
class ActionPolicy:
    allowed: frozenset[str] = frozenset({
        "open_app", "open_url", "read_clipboard", "write_clipboard",
        "type_text", "hotkey", "take_screenshot", "notify"
    })
    confirmation_required: frozenset[str] = frozenset({
        "type_text", "hotkey", "write_clipboard"
    })

class PermissionDenied(Exception):
    pass

class PermissionGate:
    def __init__(self, policy: ActionPolicy | None = None):
        self.policy = policy or ActionPolicy()

    def check(self, action: str, confirmed: bool = False) -> None:
        if action not in self.policy.allowed:
            raise PermissionDenied(f"Action not allowlisted: {action}")
        if action in self.policy.confirmation_required and not confirmed:
            raise PermissionDenied(f"Confirmation required for: {action}")
