"""Built-in structured tools. New integrations must use ToolRegistry."""
from __future__ import annotations
from dataclasses import asdict
from typing import Any, Mapping
import os
import time
from .core import JarvisTool, PermissionLevel, ToolResult
from .tasks import TaskStore

class SystemStatusTool:
    name = "system_status"; description = "Read local system resource usage."; input_schema: Mapping[str, Any] = {}; permission_level = PermissionLevel.READ_ONLY
    async def execute(self, **_: Any) -> ToolResult:
        try:
            import psutil
            memory = psutil.virtual_memory(); disk = psutil.disk_usage("/")
            data = {"cpu_percent": psutil.cpu_percent(interval=None), "memory_percent": memory.percent, "disk_percent": disk.percent, "uptime_seconds": max(0, int(time.time() - psutil.boot_time()))}
        except ImportError:
            stat = os.statvfs("/")
            data = {"cpu_percent": None, "memory_percent": None, "disk_percent": round(100 * (1 - (stat.f_bavail / stat.f_blocks)), 2), "uptime_seconds": None}
        return ToolResult(True, "System status retrieved.", data)

class CreateTaskTool:
    name = "create_task"; description = "Create a local task."; input_schema = {"title": "string"}; permission_level = PermissionLevel.LOW_RISK
    def __init__(self, store: TaskStore) -> None: self.store = store
    async def execute(self, **kwargs: Any) -> ToolResult:
        task = self.store.create(str(kwargs.get("title", "")))
        return ToolResult(True, "Task created.", {"task": asdict(task)})

class ListTasksTool:
    name = "list_tasks"; description = "List local tasks."; input_schema = {}; permission_level = PermissionLevel.READ_ONLY
    def __init__(self, store: TaskStore) -> None: self.store = store
    async def execute(self, **_: Any) -> ToolResult:
        return ToolResult(True, "Tasks retrieved.", {"tasks": [asdict(t) for t in self.store.list()]})
