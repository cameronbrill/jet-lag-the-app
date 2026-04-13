package com.jetlag.platform

import kotlin.time.Clock
import kotlin.time.ExperimentalTime

@OptIn(ExperimentalTime::class)
class TimeProvider {
    fun nowMillis(): Long = Clock.System.now().toEpochMilliseconds()
}
