"""Centralized, safe-by-default JARVIS configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:  # dotenv is optional for library users
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    return default if value is None else value.strip().lower() in {"1", "true", "yes", "on"}


def _float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True, slots=True)
class Settings:
    name: str
    log_level: str
    data_dir: Path
    ai_provider: str
    ai_api_key: str | None
    ai_base_url: str
    ai_model: str
    voice_enabled: bool
    wake_word: str
    computer_control: bool
    require_confirmation: bool
    allowed_apps: tuple[str, ...]
    allowed_hosts: tuple[str, ...]
    trading_mode: str
    live_trading: bool
    require_trade_confirmation: bool
    trading_kill_switch: bool
    daily_brief_time: str
    timezone: str
    max_risk_per_trade: float
    max_daily_loss: float
    max_open_positions: int

    @classmethod
    def from_environment(cls) -> "Settings":
        if load_dotenv:
            load_dotenv(override=False)
        mode = os.getenv("JARVIS_TRADING_MODE", os.getenv("JARVIS_MODE", "paper")).lower()
        # An invalid mode must fail closed.
        if mode not in {"paper", "live"}:
            mode = "paper"
        return cls(
            name=os.getenv("JARVIS_NAME", "JARVIS"), log_level=os.getenv("JARVIS_LOG_LEVEL", "INFO"),
            data_dir=Path(os.getenv("JARVIS_DATA_DIR", ".jarvis")).expanduser(),
            ai_provider=os.getenv("AI_PROVIDER", "openai_compatible"),
            ai_api_key=os.getenv("AI_API_KEY") or os.getenv("JARVIS_AI_API_KEY") or os.getenv("OPENAI_API_KEY"),
            ai_base_url=os.getenv("AI_BASE_URL", os.getenv("JARVIS_AI_BASE_URL", "https://api.openai.com/v1")).rstrip("/"),
            ai_model=os.getenv("AI_MODEL", os.getenv("JARVIS_AI_MODEL", "")),
            voice_enabled=_bool("JARVIS_VOICE_ENABLED", False), wake_word=os.getenv("JARVIS_WAKE_WORD", "jarvis").lower(),
            computer_control=_bool("JARVIS_COMPUTER_CONTROL", False), require_confirmation=_bool("JARVIS_REQUIRE_CONFIRMATION", True),
            allowed_apps=tuple(filter(None, os.getenv("JARVIS_ALLOWED_APPS", "calculator").split(","))),
            allowed_hosts=tuple(filter(None, os.getenv("JARVIS_ALLOWED_HOSTS", "github.com,google.com,calendar.google.com,mail.google.com,drive.google.com").split(","))),
            trading_mode=mode, live_trading=_bool("JARVIS_LIVE_TRADING", _bool("LIVE_TRADING_ENABLED", False)),
            require_trade_confirmation=_bool("JARVIS_REQUIRE_TRADE_CONFIRMATION", True), trading_kill_switch=_bool("JARVIS_TRADING_KILL_SWITCH", False),
            daily_brief_time=os.getenv("JARVIS_DAILY_BRIEF_TIME", "08:00"), timezone=os.getenv("JARVIS_TIMEZONE", "UTC"),
            max_risk_per_trade=_float("MAX_RISK_PER_TRADE", 0.01), max_daily_loss=_float("MAX_DAILY_LOSS", 0.03),
            max_open_positions=_int("MAX_OPEN_POSITIONS", 3),
        )


settings = Settings.from_environment()
