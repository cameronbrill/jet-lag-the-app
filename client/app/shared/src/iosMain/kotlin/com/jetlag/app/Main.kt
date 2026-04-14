package com.jetlag.app

import androidx.compose.ui.window.ComposeUIViewController
import com.jetlag.app.shared.JetlagApp
import platform.UIKit.UIViewController

@Suppress("unused") // Called from Swift / Xcode host (see iosApp Swift sources)
fun mainViewController(): UIViewController =
    ComposeUIViewController {
        JetlagApp()
    }
