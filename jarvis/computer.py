from .permissions import PermissionGate

class ComputerController:
    """Safe adapter boundary for local computer automation.

    Actual OS integration should be implemented separately (for example with
    platform-specific adapters). Every operation must pass the permission gate.
    """
    def __init__(self, gate: PermissionGate | None = None):
        self.gate = gate or PermissionGate()

    def open_url(self, url: str):
        self.gate.check("open_url")
        import webbrowser
        return webbrowser.open(url)

    def notify(self, message: str):
        self.gate.check("notify")
        print(f"[JARVIS] {message}")
