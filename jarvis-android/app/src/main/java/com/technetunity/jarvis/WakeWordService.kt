package com.technetunity.jarvis

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.IBinder

/**
 * JARVIS background service.
 * The microphone must be used only while the foreground service is visible to the user.
 * Replace the detector stub with a licensed offline wake-word engine to detect "Hey JARVIS".
 */
class WakeWordService : Service() {
    override fun onCreate() {
        super.onCreate()
        val channel = NotificationChannel("jarvis", "JARVIS", NotificationManager.IMPORTANCE_LOW)
        getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
        val notification = Notification.Builder(this, "jarvis")
            .setContentTitle("JARVIS active")
            .setContentText("Listening for Hey JARVIS")
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .setOngoing(true)
            .build()
        startForeground(7, notification)
        startWakeWordDetector()
    }

    private fun startWakeWordDetector() {
        // TODO: integrate an offline keyword spotter here.
        // On detection of "Hey JARVIS", launch the command-capture flow.
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int) = START_STICKY
    override fun onBind(intent: Intent?): IBinder? = null
}
