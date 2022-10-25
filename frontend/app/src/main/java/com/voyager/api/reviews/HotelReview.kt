package com.voyager.api.reviews

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class HotelReview(
    val date: String,
    val username: String,
    val stars: Int,
    val content: String
) : Parcelable