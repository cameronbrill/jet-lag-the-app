package com.jetlag.feature.creator.usecase

import kotlin.test.Test
import kotlin.test.assertEquals

class SessionTrackerTest {
    @Test
    fun elapsed_tracksDelta() {
        var t = 1000L
        val tracker = SessionTracker(TimeSource { t })
        tracker.start()
        t = 1500L
        assertEquals(500L, tracker.elapsedMillis())
    }
}
