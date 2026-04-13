package com.jetlag.feature.auth

import kotlin.test.Test
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class AuthGateTest {
    @Test
    fun signIn_setsState() {
        val gate = AuthGate()
        assertFalse(gate.isSignedIn())
        gate.signIn("abc")
        assertTrue(gate.isSignedIn())
    }
}
