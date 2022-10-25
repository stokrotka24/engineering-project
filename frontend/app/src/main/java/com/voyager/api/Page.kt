package com.voyager.api

data class Page<T>(
    val count: Int,
    val next: Any,
    val previous: String,
    val results: List<T>
)