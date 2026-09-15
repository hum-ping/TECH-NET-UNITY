from __future__ import annotations

from .assistant_core import JarvisAssistant


def run_chat() -> None:
    assistant = JarvisAssistant()
    print("JARVIS real-assistant mode online. Type 'stop jarvis' for emergency stop.")
    while not assistant.agent.stop_event.is_set():
        try:
            text = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            assistant.agent.emergency_stop()
            print("JARVIS: stopped safely.")
            return
        reply = assistant.respond(text)
        print(f"JARVIS> {reply.text}")
        if reply.action == "stop":
            return


if __name__ == "__main__":
    run_chat()
