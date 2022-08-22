package com.voyager.api.registration

data class RegisterRequest(
    val username: String,
    val email: String,
    val password: String,
    val password_confirmation: String
)