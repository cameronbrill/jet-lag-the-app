package com.jetlag.platform

import kotlin.test.Test
import kotlin.test.assertTrue

class TimeProviderTest {
    @Test
    fun nowMillis_returnsReasonableEpoch() {
        val provider = TimeProvider()
        val millis = provider.nowMillis()
        assertTrue(millis > 0, "nowMillis should be positive")
        // April 2026 epoch millis ≈ 1.77e12; sanity-check we're in the right ballpark
        assertTrue(millis > 1_700_000_000_000L, "nowMillis should be after ~Nov 2023")
    }
}
