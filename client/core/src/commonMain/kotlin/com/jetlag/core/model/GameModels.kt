package com.jetlag.core.model

import kotlinx.serialization.Serializable

@Serializable
enum class GamePhase {
    LOBBY,
    PLAYING,
    COMPLETED,
}

@Serializable
data class GameSummary(
    val id: String,
    val name: String,
    val phase: GamePhase,
    val current_round_index: Int = 0,
)

interface GameRepository {
    suspend fun getGame(id: String): GameSummary
}
