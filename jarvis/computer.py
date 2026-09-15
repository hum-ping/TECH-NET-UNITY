from __future__ import annotations

import platform
import subprocess
import webbrowser
from urllib.parse import urlparse

from .config import settings
from .permissions import PermissionGate


class ComputerController:
    """Safe local computer adapter with explicit app and URL allowlists."""

    ALLOWED_URL_HOSTS = {
        "github.com", "www.github.com", "google.com", "www.google.com",
        "calendar.google.com", "mail.google.com", "drive.google.com",
    }

    ALLOWED_APPS = {
        "notepad": ["notepad.exe"],
        "calculator": ["calc.exe"],
    }

    def __init__(self, gate: PermissionGate | None = None):
        self.gate = gate or PermissionGate()

    def system_info(self) -> dict:
        return {"os": platform.system(), "release": platform.release(), "machine": platform.machine()}

    def open_target(self, target: str, confirmed: bool = False) -> str:
        if not settings.computer_control:
            return "Computer control is disabled. Set JARVIS_COMPUTER_CONTROL=true after reviewing the allowlist."
        if target.startswith(("https://", "http://")):
            self.gate.check("open_url", confirmed=confirmed)
            parsed = urlparse(target)
            if parsed.hostname not in self.ALLOWED_URL_HOSTS:
                raise PermissionError("URL host is not on the JARVIS allowlist")
            webbrowser.open(target)
            return f"Opened {target}"
        app = target.lower().strip()
        if app not in self.ALLOWED_APPS:
            raise PermissionError("Application is not on the JARVIS allowlist")
        self.gate.check("open_app", confirmed=confirmed)
        subprocess.Popen(self.ALLOWED_APPS[app])
        return f"Opened {app}"

    def notify(self, message: str):
        self.gate.check("notify")
        print(f"[JARVIS] {message}")
