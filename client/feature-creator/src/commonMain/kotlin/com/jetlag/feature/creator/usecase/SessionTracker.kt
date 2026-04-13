package com.jetlag.feature.creator.usecase

fun interface TimeSource {
    fun nowMillis(): Long
}

class SessionTracker(
    private val timeSource: TimeSource,
) {
    private var startedAt: Long? = null

    fun start() {
        startedAt = timeSource.nowMillis()
    }

    fun elapsedMillis(): Long {
        val start = startedAt ?: return 0L
        return timeSource.nowMillis() - start
    }
}
