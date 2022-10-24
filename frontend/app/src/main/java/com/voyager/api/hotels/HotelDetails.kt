package com.voyager.api.hotels

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class HotelDetails(
    val id: Int,
    val name: String,
    val address: String,
    val city: String,
    val state: String,
    val postal_code: String,
    val stars: String,
    val review_count: Int,
    val categories: List<String>,
    val attributes: List<Attribute>?
) : Parcelable