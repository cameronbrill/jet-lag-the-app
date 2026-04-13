package com.jetlag.core.network

import com.jetlag.core.model.GameRepository
import com.jetlag.core.model.GameSummary

class RemoteGameRepository(
    private val client: JetlagApiClient,
) : GameRepository {
    override suspend fun getGame(id: String): GameSummary = client.fetchGame(id)
}
