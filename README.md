# JARVIS — DervE Trading Assistant

A local-first personal assistant designed to run on your laptop and monitor the DervE trading account.

## Safety-first status

The trading engine starts in **paper/simulation mode**. It can scan market data, calculate indicators, generate LONG/SHORT/NO-TRADE signals, backtest strategies, and enforce risk limits. Live order execution is intentionally disabled until broker/API credentials and explicit live-trading controls are configured.

No strategy can guarantee profit.

## JARVIS desktop agent

The repository now includes an always-running local agent with:

- scheduled daily routines with duplicate-run protection
- safe local notifications
- interactive console commands
- local JSON memory for short notes
- an emergency stop
- an explicit computer-action boundary and allowlist
- startup guidance for Windows, macOS, and Linux

Start the continuous agent:

```bash
python -m jarvis.start
```

Or use the interactive console from a small launcher of your choice by importing `jarvis.console.run_console`.

### Configuration

Set these optional environment variables in `.env`:

```text
JARVIS_NAME=JARVIS
JARVIS_COMPUTER_CONTROL=false
JARVIS_REQUIRE_CONFIRMATION=true
JARVIS_DAILY_BRIEF_TIME=08:00
JARVIS_TIMEZONE=Africa/Nairobi
```

The default routine sends a morning briefing, midday reminder, and end-of-day review. Work-app launching remains a deliberate extension point until specific apps are added to the allowlist.

### Startup on boot

See `jarvis/startup/README.md`. The repository does **not** silently install an OS service or grant itself computer permissions. Register `python -m jarvis.start` with your operating system after reviewing the allowlist.

### Voice

The current core is intentionally text/console-first. A microphone/STT adapter can be added without changing the permission layer; voice input should produce the same allowlisted commands as typed input.

### Emergency stop

Press `Ctrl+C` to stop the running agent. Sensitive computer actions require explicit confirmation through the permission layer; arbitrary shell commands are not supported.

## Existing capabilities

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
