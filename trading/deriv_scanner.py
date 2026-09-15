import asyncio
import json
import statistics
from collections import deque
from dataclasses import dataclass

import websockets

PUBLIC_WS = "wss://api.derivws.com/trading/v1/options/ws/public"


@dataclass
class Signal:
    symbol: str
    action: str
    price: float
    fast_ma: float
    slow_ma: float
    confidence: float


class DerivScanner:
    """Read-only Deriv market scanner. No account credentials are required."""

    def __init__(self, symbol: str = "1HZ100V", window: int = 30):
        self.symbol = symbol
        self.prices = deque(maxlen=window)
        self.fast = 7
        self.slow = 21

    def signal(self, price: float) -> Signal | None:
        self.prices.append(price)
        if len(self.prices) < self.slow:
            return None
        values = list(self.prices)
        fast_ma = statistics.fmean(values[-self.fast:])
        slow_ma = statistics.fmean(values[-self.slow:])
        spread = abs(fast_ma - slow_ma) / max(abs(slow_ma), 1e-12)
        confidence = min(0.99, 0.50 + spread * 100)
        action = "LONG" if fast_ma > slow_ma else "SHORT" if fast_ma < slow_ma else "NO-TRADE"
        return Signal(self.symbol, action, price, fast_ma, slow_ma, confidence)

    async def stream(self):
        async with websockets.connect(PUBLIC_WS, ping_interval=20, ping_timeout=20) as ws:
            await ws.send(json.dumps({"ticks": self.symbol, "subscribe": 1, "req_id": 1}))
            async for raw in ws:
                msg = json.loads(raw)
                if msg.get("msg_type") == "tick":
                    quote = float(msg["tick"]["quote"])
                    yield self.signal(quote)


async def run(symbol: str = "1HZ100V"):
    scanner = DerivScanner(symbol)
    async for signal in scanner.stream():
        if signal:
            print(signal)


if __name__ == "__main__":
    asyncio.run(run())
