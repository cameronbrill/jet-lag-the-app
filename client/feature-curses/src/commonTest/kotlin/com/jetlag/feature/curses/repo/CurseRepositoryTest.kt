package com.jetlag.feature.curses.repo

import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals

class CurseRepositoryTest {
    @Test
    fun titles_reflectsAdds() =
        runTest {
            val repo = InMemoryCurseRepository()
            repo.add("A")
            assertEquals(listOf("A"), repo.titles())
        }
}
