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
    private var listening = false

    override fun onCreate() {
        super.onCreate()
        createNotification()
        tts = TextToSpeech(this, this)
        if (SpeechRecognizer.isRecognitionAvailable(this)) {
            recognizer = SpeechRecognizer.createSpeechRecognizer(this)
            recognizer?.setRecognitionListener(this)
            startListening()
        } else {
            speak("Speech recognition is not available on this phone.")
        }
    }

    private fun createNotification() {
        val channel = NotificationChannel("jarvis", "JARVIS", NotificationManager.IMPORTANCE_LOW)
        getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
        val notification = Notification.Builder(this, "jarvis")
            .setContentTitle("JARVIS active")
            .setContentText("Listening for Hey JARVIS")
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .setOngoing(true)
            .build()
        startForeground(7, notification)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == "TEST_VOICE") speak("Hello. JARVIS voice is working.")
        return START_STICKY
    }

    private fun startListening(delay: Long = 300) {
        if (restarting || recognizer == null) return
        restarting = true
        handler.postDelayed({
            restarting = false
            try {
                listening = true
                recognizer?.startListening(Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.US.toLanguageTag())
                    putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
                    putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
                    putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 1100)
                    putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 500)
                })
            } catch (_: Exception) {
                listening = false
                scheduleRestart(700)
            }
        }, delay)
    }

    override fun onResults(results: Bundle?) {
        listening = false
        val text = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
            ?.firstOrNull()?.trim()?.lowercase(Locale.US) ?: ""
        handleRecognizedText(text)
    }

    override fun onPartialResults(partialResults: Bundle?) {
        val text = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
            ?.firstOrNull()?.trim()?.lowercase(Locale.US) ?: return
        if (!waitingForCommand && containsWakeWord(text)) {
            waitingForCommand = true
            val afterWake = text.substringAfter("jarvis", "").trim()
            if (afterWake.isNotBlank()) {
                processCommand(afterWake)
            } else {
                speak("Yes. What can I do for you?")
            }
        }
    }

    private fun handleRecognizedText(text: String) {
        if (text.isBlank()) { scheduleRestart(); return }
        if (!waitingForCommand) {
            if (containsWakeWord(text)) {
                val afterWake = text.substringAfter("jarvis", "").trim()
                waitingForCommand = afterWake.isBlank()
                if (afterWake.isBlank()) speak("Yes. What can I do for you?") else processCommand(afterWake)
            }
        } else {
            waitingForCommand = false
            processCommand(text)
        }
    }

    private fun containsWakeWord(text: String): Boolean {
        val normalized = text.replace(Regex("[^a-z0-9 ]"), " ")
            .replace(Regex("\\s+"), " ").trim()
        return normalized.contains("hey jarvis") || normalized.startsWith("jarvis")
    }

    private fun processCommand(rawCommand: String) {
        val command = rawCommand.trim().lowercase(Locale.US)
        val answer = when {
            command.contains("routine") -> "Your routine is ready. Study forex, work, exercise, and manage your personal tasks."
            command.contains("what are my tasks") || command == "tasks" || command == "show tasks" -> loadTasks()
            command.startsWith("add task") -> addTask(command.removePrefix("add task").trim())
            command.contains("hello") || command == "hi" -> "Hello. I am JARVIS, your personal Android assistant."
            command.contains("time") -> "The current time is " + java.text.SimpleDateFormat("h:mm a", Locale.US).format(java.util.Date())
            command.contains("analyze") && command.contains("eurusd") -> "EURUSD analysis needs a live market data connection. I will not invent a price or signal."
            command.contains("help") -> "You can say: Hey JARVIS, what are my tasks; add task study forex; tell me the time; or analyze EURUSD."
            else -> "I heard: $rawCommand. I can handle local commands now; an AI provider can be added later for general questions."
        }
        speak(answer)
    }

    private fun loadTasks(): String {
        val prefs = getSharedPreferences("jarvis", MODE_PRIVATE)
        val tasks = prefs.getStringSet("tasks", emptySet())?.toList().orEmpty()
        return if (tasks.isEmpty()) "You have no saved tasks." else "Your tasks are: " + tasks.joinToString(", ")
    }

    private fun addTask(task: String): String {
        if (task.isBlank()) return "Tell me the task after saying add task."
        val prefs = getSharedPreferences("jarvis", MODE_PRIVATE)
        val tasks = prefs.getStringSet("tasks", emptySet())?.toMutableSet() ?: mutableSetOf()
        tasks.add(task)
        prefs.edit().putStringSet("tasks", tasks).apply()
        return "Added task: $task."
    }

    private fun speak(text: String) {
        if (::tts.isInitialized) tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "jarvis")
        scheduleRestart(1700)
    }

    private fun scheduleRestart(delay: Long = 350) {
        waitingForCommand = false
        handler.removeCallbacksAndMessages(null)
        if (!isDestroyed) handler.postDelayed({ startListening() }, delay)
    }

    override fun onError(error: Int) {
        listening = false
        scheduleRestart(600)
    }
    override fun onReadyForSpeech(params: Bundle?) {}
    override fun onBeginningOfSpeech() {}
    override fun onRmsChanged(rmsdB: Float) {}
    override fun onBufferReceived(buffer: ByteArray?) {}
    override fun onEndOfSpeech() {}
    override fun onEvent(eventType: Int, params: Bundle?) {}

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) tts.language = Locale.US
    }

    override fun onDestroy() {
        handler.removeCallbacksAndMessages(null)
        recognizer?.cancel()
        recognizer?.destroy()
        recognizer = null
        if (::tts.isInitialized) tts.shutdown()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
