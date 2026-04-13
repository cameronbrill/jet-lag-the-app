package com.jetlag.feature.game.viewmodel

import com.jetlag.core.model.GameRepository
import com.jetlag.core.model.GameSummary
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class GameViewModel(
    private val repository: GameRepository,
) {
    private val _state = MutableStateFlow<GameSummary?>(null)
    val state: StateFlow<GameSummary?> = _state

    suspend fun load(gameId: String) {
        _state.value = repository.getGame(gameId)
    }
}
