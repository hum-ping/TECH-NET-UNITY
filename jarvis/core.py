"""Trust boundary primitives shared by every JARVIS interface and tool."""
from __future__ import annotations

import asyncio
import inspect
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Awaitable, Callable, Mapping, Protocol


class PermissionLevel(str, Enum):
    READ_ONLY = "read_only"
    LOW_RISK = "low_risk"
    USER_CONFIRMATION = "user_confirmation"
    HIGH_RISK = "high_risk"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class ToolResult:
    success: bool
    message: str
    data: Mapping[str, Any] = field(default_factory=dict)
    requires_confirmation: bool = False
    error_code: str | None = None


class JarvisTool(Protocol):
    name: str
    description: str
    input_schema: Mapping[str, Any]
    permission_level: PermissionLevel

    async def execute(self, **kwargs: Any) -> ToolResult: ...


class PermissionDenied(RuntimeError):
    """A request was stopped before a side effect occurred."""


class PermissionManager:
    """Central policy: model output is a proposal, never direct authority."""
    def authorize(self, level: PermissionLevel, *, confirmed: bool, emergency_stopped: bool) -> None:
        if emergency_stopped:
            raise PermissionDenied("Emergency stop is active; restart JARVIS before executing actions.")
        if level is PermissionLevel.BLOCKED:
            raise PermissionDenied("This operation is blocked by JARVIS security policy.")
        if level in {PermissionLevel.USER_CONFIRMATION, PermissionLevel.HIGH_RISK} and not confirmed:
            raise PermissionDenied("Explicit confirmation is required for this operation.")


class ToolRegistry:
    def __init__(self, permissions: PermissionManager | None = None) -> None:
        self._tools: dict[str, JarvisTool] = {}
        self.permissions = permissions or PermissionManager()

    def register(self, tool: JarvisTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Duplicate tool: {tool.name}")
        self._tools[tool.name] = tool

    def available(self) -> tuple[JarvisTool, ...]:
        return tuple(self._tools.values())

    async def execute(self, name: str, *, confirmed: bool = False, emergency_stopped: bool = False, **kwargs: Any) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(False, f"Unknown tool: {name}", error_code="tool_not_found")
        try:
            self.permissions.authorize(tool.permission_level, confirmed=confirmed, emergency_stopped=emergency_stopped)
            result = await tool.execute(**kwargs)
            if not isinstance(result, ToolResult):
                return ToolResult(False, "Tool returned an invalid result.", error_code="invalid_tool_result")
            return result
        except PermissionDenied as exc:
            return ToolResult(False, str(exc), requires_confirmation=tool.permission_level in {PermissionLevel.USER_CONFIRMATION, PermissionLevel.HIGH_RISK}, error_code="permission_denied")
        except (ValueError, TypeError) as exc:
            return ToolResult(False, f"Invalid tool input: {exc}", error_code="invalid_input")
        except Exception:  # tools must not take down the agent
            logging.getLogger(__name__).exception("Tool execution failed", extra={"tool": name})
            return ToolResult(False, "The requested service could not complete the operation. Please try again.", error_code="tool_failed")


@dataclass(frozen=True, slots=True)
class JarvisEvent:
    name: str
    data: Mapping[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[JarvisEvent], Any]]] = {}

    def subscribe(self, event_name: str, callback: Callable[[JarvisEvent], Any]) -> None:
        self._subscribers.setdefault(event_name, []).append(callback)

    async def publish(self, event_name: str, **data: Any) -> None:
        event = JarvisEvent(event_name, data)
        for callback in self._subscribers.get(event_name, ()) + self._subscribers.get("*", ()):
            outcome = callback(event)
            if inspect.isawaitable(outcome):
                await outcome


class EmergencyStop:
    def __init__(self) -> None:
        self.active = False

    def engage(self) -> None:
        self.active = True

    def reset(self) -> None:
        self.active = False
