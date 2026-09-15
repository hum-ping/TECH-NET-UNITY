# JARVIS — DervE Trading Assistant

A local-first personal assistant designed to run on your laptop and monitor the DervE trading account.

## Safety-first status

The trading engine starts in **paper/simulation mode**. It can scan market data, calculate indicators, generate LONG/SHORT/NO-TRADE signals, backtest strategies, and enforce risk limits. Live order execution is intentionally disabled until broker/API credentials and explicit live-trading controls are configured.

No strategy can guarantee profit.

## Planned capabilities

- Local JARVIS command interface
- Controlled laptop actions using an allowlist
- Market scanning and technical indicators
- Signal generation and trade journaling
- Backtesting and paper trading
- Risk limits, position sizing, stop-loss/take-profit rules
- DervE execution adapter when the required API/integration is available
- Emergency kill switch

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## DervE connection

Put credentials only in `.env` or your operating system's secret store. Never commit API keys to GitHub.

The repository currently contains a broker-agnostic execution interface so the exact DervE API details can be added without exposing credentials.

## Trading rollout

1. Backtest
2. Paper trade
3. Validate risk controls
4. Connect the broker/API
5. Keep live execution behind an explicit enable flag and kill switch

## License

Private project for the repository owner.
