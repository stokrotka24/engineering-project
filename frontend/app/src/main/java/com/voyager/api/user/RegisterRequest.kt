package com.voyager.api.user

data class RegisterRequest(
    val username: String,
    val email: String,
    val password: String,
    val password_confirmation: String
)