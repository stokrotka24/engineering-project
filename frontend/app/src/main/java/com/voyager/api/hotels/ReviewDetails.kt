package com.voyager.api.hotels

data class ReviewDetails(
    val date: String,
    val username: String,
    val stars: Int,
    val content: String
)