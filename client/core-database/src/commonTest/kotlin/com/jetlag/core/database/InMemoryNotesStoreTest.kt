package com.jetlag.core.database

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.joinAll
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.withContext
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

    @Test
    fun appendNote_threadSafe() =
        runTest {
            val store = InMemoryNotesStore()
            withContext(Dispatchers.Default) {
                coroutineScope {
                    (1..100)
                        .map { i ->
                            launch { store.appendNote("note-$i") }
                        }.joinAll()
                }
            }
            assertEquals(100, store.notes().size)
        }
}
