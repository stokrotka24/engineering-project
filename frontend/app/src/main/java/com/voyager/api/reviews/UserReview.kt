package com.voyager.api.reviews

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class UserReview(
    val id: Int,
    val date: String,
    val hotel_name: String,
    val stars: Int,
    val content: String
) : Parcelable