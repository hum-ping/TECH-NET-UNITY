package com.technetunity.jarvis

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.IBinder
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import java.util.Locale

class WakeWordService : Service(), RecognitionListener, TextToSpeech.OnInitListener {
    private var recognizer: SpeechRecognizer? = null
    private lateinit var tts: TextToSpeech
    private val handler = Handler(Looper.getMainLooper())
    private var waitingForCommand = false
    private var restarting = false

    override fun onCreate() {
        super.onCreate()
        createNotification()
        tts = TextToSpeech(this, this)
        if (SpeechRecognizer.isRecognitionAvailable(this)) {
            recognizer = SpeechRecognizer.createSpeechRecognizer(this)
            recognizer?.setRecognitionListener(this)
            startListening()
        }
    }

    private fun createNotification() {
        val channel = NotificationChannel("jarvis", "JARVIS", NotificationManager.IMPORTANCE_LOW)
        getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
        val notification = Notification.Builder(this, "jarvis")
            .setContentTitle("JARVIS active")
            .setContentText("Say Hey JARVIS")
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .setOngoing(true)
            .build()
        startForeground(7, notification)
    }

    private fun startListening() {
        if (restarting || recognizer == null) return
        restarting = true
        handler.postDelayed({
            restarting = false
            try {
                recognizer?.startListening(Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
                    putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
                    putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
                    putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 1200)
                    putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 500)
                })
            } catch (_: Exception) { scheduleRestart(500) }
        }, 250)
    }

    override fun onResults(results: Bundle?) {
        val text = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.firstOrNull()?.trim()?.lowercase(Locale.getDefault()) ?: ""
        handleRecognizedText(text)
    }

    override fun onPartialResults(partialResults: Bundle?) {
        val text = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.firstOrNull()?.trim()?.lowercase(Locale.getDefault()) ?: return
        if (!waitingForCommand && containsWakeWord(text)) {
            waitingForCommand = true
            speak("Yes. What can I do for you?")
        }
    }

    private fun handleRecognizedText(text: String) {
        if (text.isBlank()) { scheduleRestart(); return }
        if (!waitingForCommand) {
            if (containsWakeWord(text)) {
                waitingForCommand = true
                val afterWake = text.substringAfter("jarvis", "").trim()
                if (afterWake.isNotBlank()) processCommand(afterWake) else speak("Yes. What can I do for you?")
            }
        } else {
            waitingForCommand = false
            processCommand(text)
        }
    }

    private fun containsWakeWord(text: String): Boolean {
        val normalized = text.replace(Regex("[^a-z0-9 ]"), " ").replace(Regex("\\s+"), " ").trim()
        return normalized.contains("hey jarvis") || normalized.startsWith("jarvis")
    }

    private fun processCommand(command: String) {
        val answer = when {
            command.contains("routine") -> "Your routine is ready. You can study forex, work, exercise, and handle your personal tasks."
            command.contains("tasks") || command.contains("task") -> "You can manage your tasks from the JARVIS app."
            command.contains("hello") || command.contains("hi") -> "Hello. I am JARVIS, your personal Android assistant."
            command.contains("analyze") && command.contains("eurusd") -> "I can analyze EURUSD when live market data is connected. Trading signals are informational and should use risk limits."
            command.contains("add task") -> "Task command received."
            else -> "I heard: $command. Connect an AI provider for full natural-language answers."
        }
        speak(answer)
    }

    private fun speak(text: String) {
        if (::tts.isInitialized) tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "jarvis")
        scheduleRestart(1800)
    }

    private fun scheduleRestart(delay: Long = 300) {
        waitingForCommand = false
        handler.removeCallbacksAndMessages(null)
        handler.postDelayed({ startListening() }, delay)
    }

    override fun onError(error: Int) { scheduleRestart(500) }
    override fun onReadyForSpeech(params: Bundle?) {}
    override fun onBeginningOfSpeech() {}
    override fun onRmsChanged(rmsdB: Float) {}
    override fun onBufferReceived(buffer: ByteArray?) {}
    override fun onEndOfSpeech() {}
    override fun onEvent(eventType: Int, params: Bundle?) {}

    override fun onInit(status: Int) { if (status == TextToSpeech.SUCCESS) tts.language = Locale.US }
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int = START_STICKY

    override fun onDestroy() {
        handler.removeCallbacksAndMessages(null)
        recognizer?.destroy()
        recognizer = null
        if (::tts.isInitialized) tts.shutdown()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
