package com.voyager.api.hotels

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Hotel(
    val name: String,
    val city: String,
    val stars: Float,
    val review_count: Int,
    val categories: String,
    val recommendation_score: Int
) : Parcelable