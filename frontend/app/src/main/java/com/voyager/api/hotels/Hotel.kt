package com.voyager.api.hotels

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Hotel(
    val name: String,
    val city: String,
    val stars: Int,
    val review_count: Int,
    //TODO make categories nested object
    val categories: String
) : Parcelable