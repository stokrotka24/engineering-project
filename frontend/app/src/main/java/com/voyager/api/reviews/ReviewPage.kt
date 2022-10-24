package com.voyager.api.reviews

data class ReviewPage(
    val count: Int,
    val next: Any,
    val previous: String,
    val results: List<ReviewDetails>
)