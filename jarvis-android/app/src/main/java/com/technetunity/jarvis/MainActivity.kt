package com.technetunity.jarvis

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.speech.RecognizerIntent
import android.speech.tts.TextToSpeech
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.util.Locale

class MainActivity : ComponentActivity(), TextToSpeech.OnInitListener {
    private lateinit var tts: TextToSpeech
    private lateinit var status: TextView
    private val requestCode = 100

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        tts = TextToSpeech(this, this)
        buildUi()
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.RECORD_AUDIO), requestCode)
        }
    }

    private fun buildUi() {
        val root = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(48, 64, 48, 48) }
        val title = TextView(this).apply { text = "JARVIS"; textSize = 34f }
        status = TextView(this).apply { text = "Status: Ready"; textSize = 18f }
        val start = Button(this).apply { text = "START JARVIS"; setOnClickListener { startJarvis() } }
        val talk = Button(this).apply { text = "TALK TO JARVIS"; setOnClickListener { listen() } }
        root.addView(title); root.addView(status); root.addView(start); root.addView(talk)
        setContentView(root)
    }

    private fun startJarvis() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.RECORD_AUDIO), requestCode)
            return
        }
        ContextCompat.startForegroundService(this, Intent(this, WakeWordService::class.java))
        status.text = "Status: Listening for Hey JARVIS"
        speak("JARVIS is online. Say Hey JARVIS.")
    }

    override fun onInit(result: Int) {
        if (result == TextToSpeech.SUCCESS) { tts.language = Locale.US }
    }

    private fun speak(text: String) { tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "jarvis") }

    private fun listen() {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
            putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to JARVIS")
        }
        startActivityForResult(intent, 101)
    }

    @Deprecated("Use Activity Result API in a production app")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != 101 || resultCode != RESULT_OK) return
        val command = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)?.firstOrNull()?.lowercase() ?: return
        val answer = when {
            "routine" in command -> "Your routine is ready."
            "tasks" in command -> "Your tasks are ready."
            "analyze eurusd" in command || "eurusd" in command -> "EURUSD analysis requires current market data before I give a signal."
            "hello" in command || "hi" in command -> "Hello. I am JARVIS, your personal Android assistant."
            else -> "I heard: $command."
        }
        speak(answer)
    }

    override fun onDestroy() { tts.shutdown(); super.onDestroy() }
}
