import asyncio
import tempfile
import unittest
from pathlib import Path

from jarvis.core import PermissionLevel, ToolRegistry, ToolResult
from jarvis.memory import Memory
from trading.execution import BrokerExecution, Order, PaperBroker

class _ProtectedTool:
    name = "protected"; description = "test"; input_schema = {}; permission_level = PermissionLevel.HIGH_RISK
    async def execute(self, **kwargs): return ToolResult(True, "executed")

class SafetyCoreTests(unittest.TestCase):
    def test_high_risk_tool_requires_explicit_confirmation(self):
        registry = ToolRegistry(); registry.register(_ProtectedTool())
        blocked = asyncio.run(registry.execute("protected"))
        allowed = asyncio.run(registry.execute("protected", confirmed=True))
        self.assertFalse(blocked.success); self.assertTrue(blocked.requires_confirmation); self.assertTrue(allowed.success)

    def test_emergency_stop_blocks_even_read_actions(self):
        registry = ToolRegistry(); registry.register(_ProtectedTool())
        result = asyncio.run(registry.execute("protected", confirmed=True, emergency_stopped=True))
        self.assertFalse(result.success); self.assertEqual(result.error_code, "permission_denied")

    def test_memory_rejects_credential_labelled_content(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = Memory(Path(directory) / "memory.json")
            self.assertFalse(memory.remember("api_key=do-not-store"))
            self.assertTrue(memory.remember("prefers paper trading", "preferences"))
            self.assertEqual(memory.recall("paper"), ["prefers paper trading"])

    def test_live_order_remains_locked_by_default(self):
        receipt = BrokerExecution().submit(Order("BTC/USD", "buy", 0.01))
        self.assertEqual(receipt["status"], "blocked")

    def test_paper_orders_are_explicitly_simulated(self):
        receipt = asyncio.run(PaperBroker().place_order(Order("BTC/USD", "buy", 0.01)))
        self.assertEqual(receipt["mode"], "paper")

class ApiTests(unittest.TestCase):
    def test_health_endpoint_is_local_api_safe(self):
        from io import BytesIO
        from jarvis.api import JarvisAPI
        status = []
        body = b"".join(JarvisAPI()({"REQUEST_METHOD": "GET", "PATH_INFO": "/health", "wsgi.input": BytesIO()}, lambda value, headers: status.append(value)))
        self.assertEqual(status, ["200 OK"])
        self.assertEqual(__import__("json").loads(body), {"ok": True})
