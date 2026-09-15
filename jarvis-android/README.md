# JARVIS Android

Android JARVIS assistant with microphone activation, spoken responses, and a foreground microphone service.

## Build

The GitHub Actions workflow builds a debug APK automatically when files under `jarvis-android/` change.

Artifact: `JARVIS-debug-apk`

## Voice activation

The current implementation uses Android SpeechRecognizer as a practical wake-word approximation for “Hey JARVIS”. A dedicated offline wake-word engine can be added later for lower-power continuous keyword detection.

## Safety

Trading commands are informational/paper-mode oriented. Do not store API keys or broker credentials in the APK or source repository.

Build verification trigger: 2026-09-15.
