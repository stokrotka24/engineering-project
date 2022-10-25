package com.voyager.api.user

data class ChangePassRequest(
    val old_password: String,
    val password: String,
    val password_confirmation: String
)