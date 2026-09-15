from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

from .agent import JarvisAgent
from .memory import Memory


@dataclass
class AssistantReply:
    text: str
    action: str | None = None


class JarvisAssistant:
    """Natural-language command layer with deterministic, allowlisted execution."""

    def __init__(self):
        self.agent = JarvisAgent()
        self.memory = Memory()

    def respond(self, text: str) -> AssistantReply:
        raw = text.strip()
        lower = raw.lower()
        if not raw:
            return AssistantReply("I'm listening.")

        if any(x in lower for x in ("emergency stop", "stop jarvis", "shutdown jarvis")):
            self.agent.emergency_stop()
            return AssistantReply("Emergency stop engaged. I have stopped JARVIS safely.", "stop")

        if lower in {"hi", "hello", "hey", "good morning", "good afternoon", "good evening"}:
            return AssistantReply("Hello. JARVIS is online and ready.")

        if "who are you" in lower or "what are you" in lower:
            return AssistantReply("I am JARVIS, your local-first desktop assistant. I can manage approved routines, remember notes, report system status, and perform explicitly allowlisted computer actions.")

        if "status" in lower or "how are you" in lower:
            info = self.agent.computer.system_info()
            return AssistantReply(f"JARVIS is online. System: {info['os']} {info['release']} on {info['machine']}.")

        if lower.startswith("remember ") or lower.startswith("remember that "):
            note = re.sub(r"^remember( that)?\s+", "", raw, flags=re.I)
            self.memory.add_note(note)
            return AssistantReply("Saved that to local JARVIS memory.", "remember")

        if lower in {"what do you remember", "show memory", "memory"}:
            notes = self.memory.recent(10)
            if not notes:
                return AssistantReply("My local memory is empty.")
            return AssistantReply("Here are my recent local notes: " + "; ".join(notes))

        if lower in {"tick", "run routines", "check routines"}:
            results = self.agent.tick(datetime.now())
            return AssistantReply("Routine check complete." if not results else " ".join(str(r) for r in results), "tick")

        if lower.startswith("open "):
            return AssistantReply("I can open only an explicitly allowlisted app or HTTPS website. Use the desktop confirmation prompt before the action.", "open")

        return AssistantReply("I understood the request, but I don't have a safe allowlisted action for it yet. I can handle status, memory, routines, approved opening actions, and emergency stop.")
