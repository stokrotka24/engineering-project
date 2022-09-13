package com.voyager.api.hotels

data class HotelPage(
    val count: Int,
    val next: String,
    val previous: String,
    val results: List<Hotel>
)