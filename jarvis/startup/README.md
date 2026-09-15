# JARVIS startup

The agent can run continuously with:

```bash
python -m jarvis.start
```

To start it automatically at boot, register that command with your operating system's startup/service manager. Keep `JARVIS_COMPUTER_CONTROL=false` until you have reviewed and tested the local allowlist.

## Windows
Create a shortcut that launches `python -m jarvis.start` from the repository directory and place it in the user's Startup folder.

## macOS/Linux
Use the OS service/login mechanism to launch the same command after login. The repository intentionally does not install services automatically.

Stop the process with `Ctrl+C`; the agent exits without attempting destructive cleanup.
