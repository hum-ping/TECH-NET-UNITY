from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from .agent import JarvisAgent
from .memory import Memory


class JarvisUI:
    """Small dependency-free desktop control panel for JARVIS."""

    def __init__(self):
        self.agent = JarvisAgent()
        self.memory = Memory()
        self.root = tk.Tk()
        self.root.title("JARVIS")
        self.root.geometry("760x520")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        tk.Label(self.root, text="JARVIS", font=("Arial", 24, "bold")).pack(pady=(18, 4))
        self.status = tk.Label(self.root, text="ONLINE • local-first", font=("Arial", 11))
        self.status.pack(pady=(0, 12))

        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=20)
        tk.Label(frame, text="Command").pack(anchor="w")
        self.command = tk.Entry(frame, font=("Arial", 13))
        self.command.pack(side="left", fill="x", expand=True)
        tk.Button(frame, text="Run", command=self.run_command).pack(side="left", padx=(8, 0))

        buttons = tk.Frame(self.root)
        buttons.pack(fill="x", padx=20, pady=12)
        tk.Button(buttons, text="Status", command=lambda: self.execute("status")).pack(side="left", padx=4)
        tk.Button(buttons, text="Tick routines", command=self.tick).pack(side="left", padx=4)
        tk.Button(buttons, text="Memory", command=self.show_memory).pack(side="left", padx=4)
        tk.Button(buttons, text="EMERGENCY STOP", command=self.stop).pack(side="right", padx=4)

        self.output = tk.Text(self.root, height=20, wrap="word", state="disabled")
        self.output.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.log("JARVIS desktop control panel ready.")

    def log(self, text: str):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def execute(self, text: str, confirmed: bool = False):
        try:
            result = self.agent.run_command(text, confirmed=confirmed)
            self.log(f"> {text}\n{result}")
        except (PermissionError, ValueError) as exc:
            self.log(f"> {text}\nBLOCKED: {exc}")

    def run_command(self):
        text = self.command.get().strip()
        self.command.delete(0, "end")
        if not text:
            return
        confirmed = False
        if text.lower().startswith("open "):
            confirmed = messagebox.askyesno("Confirm action", f"Allow JARVIS to perform this action?\n\n{text}")
        self.execute(text, confirmed=confirmed)

    def tick(self):
        results = self.agent.tick()
        self.log("Routine check complete." if not results else "\n".join(results))

    def show_memory(self):
        notes = self.memory.recent()
        self.log("Memory:\n" + ("\n".join(f"- {n}" for n in notes) if notes else "(empty)"))

    def stop(self):
        self.agent.emergency_stop()
        self.status.configure(text="STOPPED • restart JARVIS to resume")
        self.log("EMERGENCY STOP engaged.")

    def close(self):
        self.agent.emergency_stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    JarvisUI().run()
