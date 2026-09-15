from trading.deriv_scanner import DerivScanner
from assistant.laptop_controller import LaptopController


class Jarvis:
    def __init__(self):
        self.laptop = LaptopController()

    def status(self) -> dict:
        return {"name": "JARVIS", "mode": "paper", "laptop": self.laptop.system_info()}

    def market_scanner(self, symbol: str = "1HZ100V") -> DerivScanner:
        return DerivScanner(symbol)

    def command(self, text: str) -> str:
        command = text.strip().lower()
        if command in {"status", "system status"}:
            return str(self.status())
        if command.startswith("open "):
            url = text.strip()[5:].strip()
            self.laptop.open_url(url)
            return f"Opened {url}"
        return "Command not allowed. JARVIS only executes explicitly implemented actions."
