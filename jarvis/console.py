from __future__ import annotations

from .agent import JarvisAgent
from .memory import Memory


HELP = "Commands: status, remember <note>, memory, tick, stop, help, exit"


def run_console() -> None:
    agent = JarvisAgent()
    memory = Memory()
    print("JARVIS console online.")
    print(HELP)
    while True:
        try:
            text = input("JARVIS> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nJARVIS stopped safely.")
            return
        lower = text.lower()
        if lower in {"exit", "quit", "stop"}:
            agent.emergency_stop()
            print("JARVIS stopped safely.")
            return
        if lower == "help":
            print(HELP)
        elif lower == "status":
            print(agent.computer.system_info())
        elif lower.startswith("remember "):
            memory.add_note(text[9:])
            print("Saved locally.")
        elif lower == "memory":
            for note in memory.recent():
                print(f"- {note}")
        elif lower == "tick":
            for result in agent.tick():
                print(result)
            print("Routine check complete.")
        else:
            print("I don't have an allowlisted action for that command.")
