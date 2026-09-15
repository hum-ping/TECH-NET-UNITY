from __future__ import annotations


class VoiceInput:
    """Optional microphone adapter. Uses speech_recognition when installed."""

    def __init__(self, wake_word: str = "jarvis"):
        self.wake_word = wake_word.lower()

    def listen_once(self) -> str | None:
        try:
            import speech_recognition as sr
        except ImportError:
            return None
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            text = recognizer.recognize_google(audio)
        except (sr.UnknownValueError, sr.RequestError):
            return None
        return text.strip()

    def command_from(self, text: str | None) -> str | None:
        if not text:
            return None
        lower = text.lower().strip()
        if self.wake_word not in lower:
            return None
        index = lower.find(self.wake_word)
        return text[index + len(self.wake_word):].strip(" ,:.-") or "status"
