package com.technetunity.jarvis

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.speech.tts.TextToSpeech
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.util.Locale

class MainActivity : AppCompatActivity() {
    private lateinit var tts: TextToSpeech
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val status = TextView(this).apply { text = "JARVIS\n\nWake word: Hey JARVIS\nStatus: Ready"; textSize = 22f; setPadding(48,80,48,48) }
        val button = Button(this).apply { text = "START JARVIS" }
        val root = android.widget.LinearLayout(this).apply { orientation = android.widget.LinearLayout.VERTICAL; addView(status); addView(button) }
        setContentView(root)
        tts = TextToSpeech(this) { if (it == TextToSpeech.SUCCESS) tts.language = Locale.US }
        button.setOnClickListener { startJarvis() }
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), 10)
    }
    private fun startJarvis() {
        startForegroundService(Intent(this, WakeWordService::class.java))
        tts.speak("JARVIS is listening for Hey JARVIS", TextToSpeech.QUEUE_FLUSH, null, "jarvis-ready")
    }
    override fun onDestroy() { tts.shutdown(); super.onDestroy() }
}
