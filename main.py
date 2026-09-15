import asyncio

from assistant.jarvis import Jarvis
from trading.deriv_scanner import run


if __name__ == "__main__":
    jarvis = Jarvis()
    print(jarvis.status())
    print("Starting Deriv public market scanner in read-only mode...")
    asyncio.run(run())
