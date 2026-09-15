# JARVIS startup

The local agent runs continuously with:

```bash
python -m jarvis.start
```

The voice loop is optional:

```bash
python -m jarvis.voice_loop
```

Voice commands are ignored unless the wake word is detected. Computer actions remain allowlisted and sensitive actions require confirmation.

## Windows
Create a Startup shortcut that launches `python -m jarvis.start` from the repository directory. For voice mode, launch `python -m jarvis.voice_loop` instead.

## macOS
Use Login Items or a user LaunchAgent to start the same command after login. Grant microphone permission only if using voice mode.

## Linux
Copy `jarvis.desktop` into `~/.config/autostart/` and edit `Exec=` to use the absolute path to the repository's Python interpreter. Grant microphone permissions only if using voice mode.

## Emergency stop
Press `Ctrl+C` in the running terminal. The agent exits safely without destructive cleanup.

## Safety
Keep `JARVIS_COMPUTER_CONTROL=false` until the local allowlist has been reviewed. Never put API keys in Git. Live trading remains disabled by default.
