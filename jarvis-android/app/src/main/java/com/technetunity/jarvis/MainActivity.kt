package com.technetunity.jarvis

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : ComponentActivity() {
    companion object { private const val REQUEST_PERMISSIONS = 100 }

    private lateinit var status: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(48, 64, 48, 48)
        }

        val title = TextView(this).apply {
            text = "JARVIS"
            textSize = 34f
        }
        val subtitle = TextView(this).apply {
            text = "Personal Android Assistant"
            textSize = 18f
        }
        status = TextView(this).apply {
            text = "Ready — tap Activate, then say: Hey JARVIS"
            textSize = 17f
        }

        val activate = Button(this).apply {
            text = "ACTIVATE JARVIS"
            setOnClickListener { startJarvis() }
        }
        val stop = Button(this).apply {
            text = "STOP JARVIS"
            setOnClickListener {
                stopService(Intent(this@MainActivity, WakeWordService::class.java))
                status.text = "JARVIS stopped"
            }
        }
        val test = Button(this).apply {
            text = "TEST VOICE"
            setOnClickListener {
                startService(Intent(this@MainActivity, WakeWordService::class.java).setAction("TEST_VOICE"))
                status.text = "Voice test sent"
            }
        }

        root.addView(title)
        root.addView(subtitle)
        root.addView(status)
        root.addView(activate)
        root.addView(stop)
        root.addView(test)
        setContentView(root)

        requestPermissionsIfNeeded()
    }

    private fun requestPermissionsIfNeeded() {
        val needed = mutableListOf<String>()
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            needed.add(Manifest.permission.RECORD_AUDIO)
        }
        if (android.os.Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            needed.add(Manifest.permission.POST_NOTIFICATIONS)
        }
        if (needed.isNotEmpty()) ActivityCompat.requestPermissions(this, needed.toTypedArray(), REQUEST_PERMISSIONS)
    }

    private fun startJarvis() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            requestPermissionsIfNeeded()
            status.text = "Microphone permission is required"
            return
        }
        ContextCompat.startForegroundService(this, Intent(this, WakeWordService::class.java))
        status.text = "JARVIS active — say Hey JARVIS"
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_PERMISSIONS && grantResults.any { it == PackageManager.PERMISSION_GRANTED }) startJarvis()
    }
}
