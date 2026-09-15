from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class RoutineTask:
    time: str
    name: str
    command: str
    requires_confirmation: bool = False

DEFAULT_ROUTINE = (
    RoutineTask("08:00", "Morning briefing", "briefing"),
    RoutineTask("08:15", "Open work apps", "open_work_apps"),
    RoutineTask("12:30", "Midday reminder", "notify_midday"),
    RoutineTask("17:30", "End-of-day review", "daily_review"),
)

def due_tasks(now: datetime, tasks=DEFAULT_ROUTINE):
    current = now.strftime("%H:%M")
    return [task for task in tasks if task.time == current]
