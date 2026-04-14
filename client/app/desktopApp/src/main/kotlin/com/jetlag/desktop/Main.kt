package com.jetlag.desktop

import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import com.jetlag.app.shared.JetlagApp

fun main() =
    application {
        Window(onCloseRequest = ::exitApplication, title = "Jet Lag") {
            JetlagApp()
        }
    }
