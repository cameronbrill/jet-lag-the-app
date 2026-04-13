package com.jetlag.core.database

import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals

class InMemoryNotesStoreTest {
    @Test
    fun appendAndRetrieveNotes() =
        runTest {
            val store = InMemoryNotesStore()
            assertEquals(emptyList(), store.notes())

            store.appendNote("first")
            store.appendNote("second")
            assertEquals(listOf("first", "second"), store.notes())
        }
}
