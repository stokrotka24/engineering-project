package com.voyager.api.user

data class RegisterErrors(
    val username: List<String>?,
    val email: List<String>?,
    val password: List<String>?,
    val password_confirmation: List<String>?
)