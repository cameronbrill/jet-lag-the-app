package com.jetlag.feature.auth

class AuthGate {
    private var token: String? = null

    fun signIn(newToken: String) {
        token = newToken
    }

    fun isSignedIn(): Boolean = token != null
}
