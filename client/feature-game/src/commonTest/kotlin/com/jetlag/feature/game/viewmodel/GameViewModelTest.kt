package com.jetlag.feature.game.viewmodel

import app.cash.turbine.test
import com.jetlag.core.model.GamePhase
import com.jetlag.core.model.GameRepository
import com.jetlag.core.model.GameSummary
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals

private class FakeRepo(
    private val summary: GameSummary,
) : GameRepository {
    override suspend fun getGame(id: String): GameSummary = summary
}

class GameViewModelTest {
    @Test
    fun load_emitsGame() =
        runTest {
            val summary = GameSummary(id = "1", name = "Test", phase = GamePhase.PLAYING)
            val vm = GameViewModel(FakeRepo(summary))
            vm.load("1")
            vm.state.test {
                assertEquals(summary, awaitItem())
            }
        }
}
