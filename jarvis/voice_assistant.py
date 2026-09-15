from __future__ import annotations

import time

from .assistant_core import JarvisAssistant
from .tts import Speaker
from .voice import VoiceInput


def run_voice_assistant() -> None:
    assistant = JarvisAssistant()
    voice = VoiceInput()
    speaker = Speaker()
    print("JARVIS voice assistant online. Say 'Jarvis' followed by a request.")
    try:
        while not assistant.agent.stop_event.is_set():
            try:
                heard = voice.listen_once()
            except Exception as exc:
                print(f"JARVIS microphone warning: {exc}")
                time.sleep(1)
                continue
            command = voice.command_from(heard)
            if not command:
                continue
            print(f"You: {command}")
            reply = assistant.respond(command)
            print(f"JARVIS: {reply.text}")
            speaker.say(reply.text)
            if reply.action == "stop":
                return
    except (KeyboardInterrupt, EOFError):
        assistant.agent.emergency_stop()
        print("JARVIS voice assistant stopped safely.")


if __name__ == "__main__":
    run_voice_assistant()
