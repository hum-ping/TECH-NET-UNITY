from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import requests

from .assistant_core import JarvisAssistant


SYSTEM_PROMPT = """You are JARVIS, a concise, helpful desktop assistant. You may reason and answer questions, but computer actions must remain inside the application's explicit allowlist and confirmation gates. Never invent successful actions. Never execute arbitrary shell commands. Never place or expose secrets in memory, logs, prompts, or replies. Trading is paper-only unless the existing project explicitly enables a safe, separately gated workflow."""


@dataclass
class BrainResponse:
    text: str
    tool: str | None = None
    arguments: dict[str, Any] | None = None


class AIClient:
    """OpenAI-compatible HTTP client. Provider endpoint is configurable."""

    def __init__(self):
        self.api_key = os.getenv("JARVIS_AI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("JARVIS_AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.model = os.getenv("JARVIS_AI_MODEL", "gpt-5.6-mini")

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def chat(self, messages: list[dict[str, str]]) -> str:
        if not self.configured:
            raise RuntimeError("AI brain is not configured. Set JARVIS_AI_API_KEY or OPENAI_API_KEY.")
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "messages": messages, "temperature": 0.2},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()


class JarvisBrain:
    """AI conversation layer with local deterministic action fallback."""

    def __init__(self):
        self.local = JarvisAssistant()
        self.client = AIClient()
        self.history: list[dict[str, str]] = []

    def respond(self, text: str) -> BrainResponse:
        text = text.strip()
        if not text:
            return BrainResponse("I'm listening.")

        # Safety-critical controls bypass the model entirely.
        if any(term in text.lower() for term in ("emergency stop", "stop jarvis", "shutdown jarvis")):
            reply = self.local.respond(text)
            return BrainResponse(reply.text, reply.action)

        if not self.client.configured:
            reply = self.local.respond(text)
            return BrainResponse(reply.text, reply.action)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.history[-12:])
        messages.append({"role": "user", "content": text})
        answer = self.client.chat(messages)
        self.history.extend([
            {"role": "user", "content": text},
            {"role": "assistant", "content": answer},
        ])
        self.history = self.history[-20:]
        return BrainResponse(answer)
