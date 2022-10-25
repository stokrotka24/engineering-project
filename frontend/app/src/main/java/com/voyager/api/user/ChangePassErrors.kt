package com.voyager.api.user

data class ChangePassErrors(
    val old_password: List<String>?,
    val password: List<String>?,
    val password_confirmation: List<String>?
)