package com.jetlag.core.database

interface NotesStore {
    suspend fun appendNote(text: String)

    suspend fun notes(): List<String>
}
