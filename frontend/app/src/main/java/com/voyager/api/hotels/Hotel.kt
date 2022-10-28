package com.voyager.api.hotels

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Hotel(
    val id: Int,
    val name: String,
    val city: String,
    var stars: Float,
    var review_count: Int,
    val categories: List<String>,
    val recommendation_score: Int
) : Parcelable