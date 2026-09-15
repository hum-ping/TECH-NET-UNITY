package com.technetunity.jarvis

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.IBinder

class WakeWordService : Service() {
    override fun onCreate() {
        super.onCreate()
        val channel = NotificationChannel("jarvis", "JARVIS", NotificationManager.IMPORTANCE_LOW)
        getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
        val notification = Notification.Builder(this, "jarvis")
            .setContentTitle("JARVIS active")
            .setContentText("Listening for Hey JARVIS")
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .build()
        startForeground(7, notification)
        // Production note: plug a real offline wake-word engine here (e.g. Porcupine/OpenWakeWord).
        // After detection, start SpeechRecognizer for the user's command and route it to the AI backend.
    }
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int) = START_STICKY
    override fun onBind(intent: Intent?): IBinder? = null
}
