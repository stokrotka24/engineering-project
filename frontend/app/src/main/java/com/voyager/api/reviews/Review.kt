package com.voyager.api.reviews

data class Review(
    val user_id: Int? = null,
    val hotel_id: Int,
    val stars: Int,
    val content: String
)