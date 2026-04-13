package com.jetlag.core.database

import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock

class InMemoryNotesStore : NotesStore {
    private val mutex = Mutex()
    private val store = mutableListOf<String>()

    override suspend fun appendNote(text: String) {
        mutex.withLock { store.add(text) }
    }

    override suspend fun notes(): List<String> = mutex.withLock { store.toList() }
}
