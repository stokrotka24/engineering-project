package com.voyager.api.hotels

data class Review(
    val user_id: Int? = null,
    val hotel_id: Int,
    val stars: Int,
    val content: String
)