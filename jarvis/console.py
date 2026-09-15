from __future__ import annotations

from .agent import JarvisAgent
from .memory import Memory


HELP = "Commands: status, remember <note>, memory, open <allowlisted app/url>, tick, stop, help, exit"


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
        if lower in {"exit", "quit", "stop", "emergency stop"}:
            agent.emergency_stop()
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
                if result:
                    print(result)
            print("Routine check complete.")
        elif lower.startswith("open "):
            confirm = input("Confirm this allowlisted computer action? [y/N] ").strip().lower() == "y"
            try:
                print(agent.run_command(text, confirmed=confirm))
            except (PermissionError, ValueError) as exc:
                print(f"Blocked: {exc}")
        else:
            print("I don't have an allowlisted action for that command.")
