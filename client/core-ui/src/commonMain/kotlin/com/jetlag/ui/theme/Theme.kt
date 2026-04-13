package com.jetlag.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable

private val colors = darkColorScheme()

@Composable
fun JetlagTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = colors, content = content)
}
