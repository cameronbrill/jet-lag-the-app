package com.jetlag.core.network

import com.jetlag.core.model.GameSummary
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.get

class JetlagApiClient(
    private val httpClient: HttpClient,
    private val baseUrl: String,
) {
    suspend fun fetchGame(gameId: String): GameSummary {
        val url = "$baseUrl/api/games/$gameId"
        return httpClient.get(url).body()
    }
}
