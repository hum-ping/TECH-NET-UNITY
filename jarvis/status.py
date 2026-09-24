from __future__ import annotations
from typing import Any
from .config import Settings, settings

def system_status(config: Settings = settings, *, emergency_stopped: bool = False) -> dict[str, Any]:
    return {"jarvis": "stopped" if emergency_stopped else "online", "ai": "configured" if config.ai_api_key else "not_configured", "voice": "enabled" if config.voice_enabled else "disabled", "computer_control": "enabled" if config.computer_control and not emergency_stopped else "disabled", "trading": "disabled" if config.trading_kill_switch else config.trading_mode, "scheduler": "running" if not emergency_stopped else "stopped", "memory": "ready", "notifications": "ready"}
