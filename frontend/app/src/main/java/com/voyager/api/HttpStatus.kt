package com.voyager.api

enum class HttpStatus(val code: Int) {
    OK(200),
    Created(201),
    NoContent(204),
    BadRequest(400),
    Unauthorized(401)
}

