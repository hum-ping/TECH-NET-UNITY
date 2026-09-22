# JARVIS — local-first AI orchestration layer

JARVIS is a modular personal-assistant foundation for local commands, optional AI conversation and voice, task routines, system monitoring, and safety-first market analysis. It is **not** an unrestricted autonomous program: every side effect is constrained by a centralized permission boundary.

> **Security notice:** a credential was included in an earlier request. Treat it as compromised: revoke/rotate it in the provider dashboard. Do not put it in source control, logs, screenshots, or this repository.

## Architecture

- `jarvis/core.py`: permission levels, structured tool results, tool registry, event bus, and emergency-stop state.
- `jarvis/config.py`: the single environment configuration boundary; safe defaults disable computer control, voice, and live trading.
- `jarvis/agent.py`: local agent, routines, observable status, and emergency-stop orchestration.
- `jarvis/tools.py`, `jarvis/tasks.py`, `jarvis/memory.py`: structured local tools, persisted tasks, and categorized secret-resistant memory.
- `jarvis/providers.py`, `jarvis/brain.py`: replaceable AI/STT/TTS/notification interfaces and an OpenAI-compatible AI adapter.
- `trading/`: read-only Deriv scanner, risk checks, paper broker, and a broker protocol. No live adapter is provided.
- `jarvis-android/`: a client-side voice shell; it must call a secured JARVIS API rather than own credentials or trading authority.

## Install and run

Requires Python 3.10+ (the code uses modern union type syntax). Create a virtual environment, install dependencies, then create a private `.env`:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m jarvis.desktop
# or: python -m jarvis.ai_chat
# or: python -m jarvis.start
```

`main.py` starts the legacy read-only public market scanner. It requires network connectivity and never sends an order.

## Configuration

All variables are documented as empty/placeholders in [`.env.example`](.env.example). The central `Settings.from_environment()` loader accepts legacy `JARVIS_AI_*` and `LIVE_TRADING_ENABLED` variables for compatibility, but new configuration should use `AI_*`, `JARVIS_TRADING_MODE`, and `JARVIS_LIVE_TRADING`.

- **AI:** Set `AI_API_KEY`, `AI_BASE_URL`, and `AI_MODEL` only in your private environment. When no key is configured, local commands keep working and AI chat reports a configuration-free local response.
- **Voice:** Set `JARVIS_VOICE_ENABLED=true` only after installing microphone dependencies; `JARVIS_WAKE_WORD` defaults to `jarvis`.
- **Computer control:** defaults to disabled. Enable `JARVIS_COMPUTER_CONTROL=true` only with reviewed `JARVIS_ALLOWED_APPS` and `JARVIS_ALLOWED_HOSTS`. URLs must use HTTPS; arbitrary shell commands are not available.
- **Trading:** defaults to `paper`, with `JARVIS_LIVE_TRADING=false` and trade confirmation on. The kill switch blocks submissions even when another setting is unsafe.

## Security model

Model and external-content output are untrusted proposals. JARVIS processes actions as:

```text
intent → structured tool request → schema/input validation → permission check
→ explicit confirmation when required → tool execution → structured result
```

`READ_ONLY` and `LOW_RISK` operations are separated from `USER_CONFIRMATION` and `HIGH_RISK` operations. Blocked operations and arbitrary shell execution are never exposed. Memory refuses common credential-labelled content; it is local JSON only and should not be treated as a secret vault.

## Tools, tasks, and routines

Tools expose a name, description, input schema, permission level, and async `execute()` method, returning `ToolResult` rather than uncaught exceptions. Local task data and routine duplicate-run state persist on disk. The scheduler only runs configured local reminders; it never silently launches privileged operations.

## Observability and emergency stop

`JarvisAgent.status()` exposes a UI/CLI-safe status object without secrets. Logs use rotating local files when `jarvis.logging.configure_logging()` is called. Press `Ctrl+C`, use the desktop **EMERGENCY STOP** button, or issue `stop jarvis`: JARVIS stops routines and blocks later action execution until restart. It does not delete data.

## Testing

```bash
python -m unittest discover -s tests -v
python -m compileall -q jarvis trading assistant
```

## Troubleshooting

- **AI unavailable:** verify private environment variables; local commands still work.
- **Voice unavailable:** install optional PyAudio/SpeechRecognition system prerequisites or use text.
- **Market provider unavailable:** the scanner reports a connection failure; no order is attempted.
- **Computer action blocked:** this is expected until control is enabled, the target is allowlisted, and confirmation is given.

## Android and UI integration

The desktop UI is intentionally small. A future UI/API should consume `JarvisAgent.status()`, structured tool results, events, tasks, and trading status. Do not embed provider or broker credentials in Android builds. Authenticate remote endpoints before exposing status, chat, or emergency-stop controls.

## Local API

Start the optional local-only API with `python -m jarvis.api`. It binds to `127.0.0.1:8765` by default and returns JSON for `GET /health`, `GET /status`, `GET/POST /tasks`, `POST /chat`, `POST /command`, and `POST /emergency-stop`. It deliberately has no remote authentication layer, so do **not** expose it beyond loopback without an authenticated reverse proxy or equivalent local security boundary.
