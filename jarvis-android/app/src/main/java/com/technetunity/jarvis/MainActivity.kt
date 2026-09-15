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
    private val requestCode = 100

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val root = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(48, 64, 48, 48) }
        val title = TextView(this).apply { text = "JARVIS"; textSize = 34f }
        val status = TextView(this).apply { text = "Say: Hey JARVIS"; textSize = 18f }
        val start = Button(this).apply { text = "ACTIVATE JARVIS"; setOnClickListener { startJarvis(); status.text = "JARVIS active — say Hey JARVIS" } }
        val stop = Button(this).apply { text = "STOP JARVIS"; setOnClickListener { stopService(Intent(this@MainActivity, WakeWordService::class.java)); status.text = "JARVIS stopped" } }
        root.addView(title); root.addView(status); root.addView(start); root.addView(stop)
        setContentView(root)
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.RECORD_AUDIO), requestCode)
        }
    }

    private fun startJarvis() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.RECORD_AUDIO), requestCode)
            return
        }
        ContextCompat.startForegroundService(this, Intent(this, WakeWordService::class.java))
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == this.requestCode && grantResults.firstOrNull() == PackageManager.PERMISSION_GRANTED) startJarvis()
    }
}
