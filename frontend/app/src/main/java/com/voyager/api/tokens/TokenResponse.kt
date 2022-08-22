package com.voyager.api.tokens

data class TokenResponse(
    val access: String,
    val refresh: String
)