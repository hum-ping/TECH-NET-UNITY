from __future__ import annotations

from .agent import JarvisAgent
from .voice import VoiceInput


def run_voice_loop() -> None:
    agent = JarvisAgent()
    voice = VoiceInput()
    print("JARVIS voice mode online. Say 'Jarvis' followed by a command.")
    print("Press Ctrl+C for emergency stop.")
    try:
        while not agent.stop_event.is_set():
            command = voice.command_from(voice.listen_once())
            if not command:
                continue
            print(f"You: {command}")
            try:
                result = agent.run_command(command)
                if result == "STOP_REQUESTED":
                    agent.emergency_stop()
                else:
                    print(f"JARVIS: {result}")
            except (PermissionError, ValueError) as exc:
                print(f"JARVIS blocked the action: {exc}")
    except (KeyboardInterrupt, EOFError):
        agent.emergency_stop()
        print("JARVIS voice mode stopped safely.")


if __name__ == "__main__":
    run_voice_loop()
