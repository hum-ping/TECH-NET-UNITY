from __future__ import annotations

from .brain import JarvisBrain


def run_ai_chat() -> None:
    brain = JarvisBrain()
    print("JARVIS V2 AI mode online. Type 'exit' to leave or 'stop jarvis' for emergency stop.")
    if not brain.client.configured:
        print("AI provider key not configured; local command mode will be used.")

    while True:
        try:
            text = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("JARVIS: session ended safely.")
            return
        if text.lower() in {"exit", "quit"}:
            return
        reply = brain.respond(text)
        print(f"JARVIS> {reply.text}")
        if reply.tool == "stop":
            return


if __name__ == "__main__":
    run_ai_chat()
