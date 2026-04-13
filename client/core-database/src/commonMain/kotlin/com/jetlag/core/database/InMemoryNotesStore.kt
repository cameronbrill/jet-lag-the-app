package com.jetlag.core.database

class InMemoryNotesStore : NotesStore {
    private val store = mutableListOf<String>()

    override suspend fun appendNote(text: String) {
        store.add(text)
    }

    override suspend fun notes(): List<String> = store.toList()
}
