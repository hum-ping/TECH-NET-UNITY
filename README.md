# JARVIS — DervE Trading Assistant

A local-first personal assistant designed to run on your laptop and monitor the DervE trading account.

## Safety-first status

The trading engine starts in **paper/simulation mode**. It can scan market data, calculate indicators, generate LONG/SHORT/NO-TRADE signals, backtest strategies, and enforce risk limits. Live order execution is intentionally disabled until broker/API credentials and explicit live-trading controls are configured.

No strategy can guarantee profit.

## JARVIS desktop agent

The repository includes an always-running local agent with:

- desktop control panel (`python -m jarvis.desktop`)
- scheduled daily routines with duplicate-run protection
- safe local notifications
- interactive console commands
- local JSON memory for short notes
- optional microphone/wake-word command mode
- allowlisted website and application control
- confirmation prompts for desktop actions
- emergency stop
- startup templates for Windows and Linux, plus macOS guidance

Start the background agent:

```bash
python -m jarvis.start
```

Start the desktop control panel:

```bash
python -m jarvis.desktop
```

Start optional voice mode:

```bash
python -m jarvis.voice_loop
```

### Configuration

Set these optional environment variables in `.env`:

```text
JARVIS_NAME=JARVIS
JARVIS_COMPUTER_CONTROL=false
JARVIS_REQUIRE_CONFIRMATION=true
JARVIS_DAILY_BRIEF_TIME=08:00
JARVIS_TIMEZONE=Africa/Nairobi
JARVIS_WAKE_WORD=jarvis
```

Computer control is deliberately **off by default**. When enabled, JARVIS can only use explicitly allowlisted applications and website hosts; it does not execute arbitrary shell commands.

### Startup on boot

See `jarvis/startup/README.md`. The repository does **not** silently install an OS service or grant itself computer or microphone permissions. Register the launcher with your operating system after reviewing the allowlist.

### Voice

Voice input is an optional adapter using SpeechRecognition/PyAudio. It listens for the wake word and sends recognized commands through the same JARVIS permission boundary used by typed commands.

### Emergency stop

Press `Ctrl+C` in the background or voice process, or use the desktop panel's **EMERGENCY STOP** button. JARVIS does not perform destructive cleanup during shutdown.

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
python -m jarvis.desktop
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
