"""Broker boundary. This module never enables live orders implicitly."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Protocol

@dataclass(frozen=True, slots=True)
class Order:
    symbol: str; side: str; quantity: float; stop_loss: float | None = None; take_profit: float | None = None

class BrokerAdapter(Protocol):
    async def get_account(self) -> dict: ...
    async def get_positions(self) -> list[dict]: ...
    async def get_orders(self) -> list[dict]: ...
    async def place_order(self, order: Order) -> dict: ...
    async def cancel_order(self, order_id: str) -> dict: ...

class BrokerExecution:
    """Compatibility guard for unfinished broker integrations."""
    def __init__(self, live_enabled: bool = False, require_confirmation: bool = True, kill_switch: bool = False):
        self.live_enabled, self.require_confirmation, self.kill_switch = live_enabled, require_confirmation, kill_switch
    def submit(self, order: Order, *, confirmed: bool = False) -> dict:
        if self.kill_switch: return {"status": "blocked", "reason": "Trading kill switch is active.", "order": asdict(order)}
        if not self.live_enabled: return {"status": "blocked", "reason": "Live trading is disabled; use paper trading first.", "order": asdict(order)}
        if self.require_confirmation and not confirmed: return {"status": "confirmation_required", "reason": "Explicit trade confirmation is required.", "order": asdict(order)}
        raise NotImplementedError("A reviewed BrokerAdapter is required before any live order can execute.")

class PaperBroker:
    """Local simulation only; its receipts are explicitly marked paper."""
    def __init__(self) -> None: self.orders: list[dict] = []
    async def get_account(self) -> dict: return {"mode": "paper", "equity": 0.0}
    async def get_positions(self) -> list[dict]: return []
    async def get_orders(self) -> list[dict]: return list(self.orders)
    async def place_order(self, order: Order) -> dict:
        receipt = {"status": "accepted", "mode": "paper", "order": asdict(order)}; self.orders.append(receipt); return receipt
    async def cancel_order(self, order_id: str) -> dict: return {"status": "not_found", "mode": "paper", "order_id": order_id}
