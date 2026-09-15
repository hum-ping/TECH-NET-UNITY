from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    symbol: str
    side: str
    quantity: float
    stop_loss: float | None = None
    take_profit: float | None = None


class BrokerExecution:
    """Broker interface. Live execution is deliberately disabled by default."""

    def __init__(self, live_enabled: bool = False):
        self.live_enabled = live_enabled

    def submit(self, order: Order) -> dict:
        if not self.live_enabled:
            return {
                "status": "blocked",
                "reason": "Live trading is disabled; use paper trading first.",
                "order": order.__dict__,
            }
        raise NotImplementedError("DervE API adapter must be implemented and reviewed before live trading.")
