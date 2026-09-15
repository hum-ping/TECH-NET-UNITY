from dataclasses import dataclass


@dataclass(frozen=True)
class RiskConfig:
    risk_per_trade: float = 0.01
    max_daily_loss: float = 0.03
    max_open_positions: int = 3


class RiskManager:
    """Hard safety checks for paper/live execution adapters."""

    def __init__(self, config: RiskConfig | None = None):
        self.config = config or RiskConfig()

    def can_open(self, equity: float, open_positions: int, daily_pnl: float) -> tuple[bool, str]:
        if equity <= 0:
            return False, "Invalid account equity"
        if open_positions >= self.config.max_open_positions:
            return False, "Maximum open positions reached"
        if daily_pnl <= -(equity * self.config.max_daily_loss):
            return False, "Daily loss limit reached"
        return True, "OK"

    def position_risk_amount(self, equity: float) -> float:
        return max(0.0, equity * self.config.risk_per_trade)
