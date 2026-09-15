# JARVIS Android Assistant

Android starter project for a voice assistant activated by **Hey JARVIS**.

## Current architecture
- Android Kotlin app
- Microphone permission
- Foreground microphone service
- Text-to-speech confirmation
- Wake-word service scaffold

## Important
The service is intentionally a scaffold: a production wake word requires an actual on-device wake-word engine. Android also restricts background microphone access, so the app must run as a visible foreground service with the required permissions/notifications.

## Next implementation
1. Add an offline wake-word engine and a custom `Hey JARVIS` model.
2. Detect the wake word continuously in the foreground service.
3. Stop wake-word capture and run Android `SpeechRecognizer` for the command.
4. Send the command to an AI backend.
5. Speak the answer with Android TTS.
6. Add routines/tasks and safe forex analysis commands.

Never put an AI API key directly in the Android APK; use a server-side backend.
