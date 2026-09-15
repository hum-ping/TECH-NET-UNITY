from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    name: str = os.getenv("JARVIS_NAME", "JARVIS")
    computer_control: bool = os.getenv("JARVIS_COMPUTER_CONTROL", "false").lower() == "true"
    require_confirmation: bool = os.getenv("JARVIS_REQUIRE_CONFIRMATION", "true").lower() == "true"
    daily_brief_time: str = os.getenv("JARVIS_DAILY_BRIEF_TIME", "08:00")
    timezone: str = os.getenv("JARVIS_TIMEZONE", "Africa/Nairobi")

settings = Settings()
