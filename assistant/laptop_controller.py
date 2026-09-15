import platform
import subprocess
from pathlib import Path


class LaptopController:
    """Allowlisted local actions only; never executes arbitrary user-supplied shell text."""

    def __init__(self, allowed_dirs: list[str] | None = None):
        self.allowed_dirs = [Path(p).expanduser().resolve() for p in (allowed_dirs or ["."])]

    def system_info(self) -> dict:
        return {"os": platform.system(), "release": platform.release(), "machine": platform.machine()}

    def open_url(self, url: str) -> None:
        if not (url.startswith("https://") or url.startswith("http://")):
            raise ValueError("Only HTTP(S) URLs are allowed")
        if platform.system() == "Windows":
            subprocess.Popen(["cmd", "/c", "start", "", url])
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", url])
        else:
            subprocess.Popen(["xdg-open", url])

    def list_allowed_files(self, directory: str = ".") -> list[str]:
        target = Path(directory).expanduser().resolve()
        if not any(target == root or root in target.parents for root in self.allowed_dirs):
            raise PermissionError("Directory is outside the JARVIS allowlist")
        return [p.name for p in target.iterdir()]
