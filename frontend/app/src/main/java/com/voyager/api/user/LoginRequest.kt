package com.voyager.api.user

data class LoginRequest(
    val email: String,
    val password: String
)