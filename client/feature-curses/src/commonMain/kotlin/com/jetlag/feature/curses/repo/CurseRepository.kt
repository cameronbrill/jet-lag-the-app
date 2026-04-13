package com.jetlag.feature.curses.repo

interface CurseRepository {
    suspend fun titles(): List<String>
}

class InMemoryCurseRepository(
    private val items: MutableList<String> = mutableListOf(),
) : CurseRepository {
    fun add(title: String) {
        items += title
    }

    override suspend fun titles(): List<String> = items.toList()
}
