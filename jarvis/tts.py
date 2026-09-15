from __future__ import annotations


class Speaker:
    """Optional text-to-speech adapter using pyttsx3 when installed."""

    def __init__(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
        except Exception:
            self.engine = None

    def say(self, text: str) -> None:
        if self.engine is None:
            return
        self.engine.say(text)
        self.engine.runAndWait()
