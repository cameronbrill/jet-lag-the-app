package com.jetlag.core.model

import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import kotlin.test.Test
import kotlin.test.assertEquals

class GameModelsTest {
    @Test
    fun gameSummary_defaultRoundIndex() {
        val summary = GameSummary(id = "g1", name = "Test Game", phase = GamePhase.LOBBY)
        assertEquals(0, summary.current_round_index)
    }

    @Test
    fun gameSummary_retainsValues() {
        val summary =
            GameSummary(
                id = "g2",
                name = "Finals",
                phase = GamePhase.PLAYING,
                current_round_index = 3,
            )
        assertEquals("g2", summary.id)
        assertEquals("Finals", summary.name)
        assertEquals(GamePhase.PLAYING, summary.phase)
        assertEquals(3, summary.current_round_index)
    }

    @Test
    fun gameSummary_serializesAndDeserializes() {
        val original =
            GameSummary(
                id = "g3",
                name = "Semi",
                phase = GamePhase.COMPLETED,
                current_round_index = 2,
            )
        val json = Json.encodeToString(original)
        val decoded = Json.decodeFromString<GameSummary>(json)
        assertEquals(original, decoded)
    }
}
