package com.voyager.api

import com.voyager.*
import com.voyager.api.login.LoginRequest
import com.voyager.api.registration.RegisterRequest
import com.voyager.api.registration.RegisterResponse
import com.voyager.api.tokens.TokenResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {
    @GET("hello/")
    fun getHello(): Call<ServerHello>

    @POST("hello/")
    fun postHello(@Body clientHello: ClientHello): Call<ServerHello>

    @POST("register/")
    fun register(@Body registerRequest: RegisterRequest): Call<RegisterResponse>

    @POST("login/")
    fun login(@Body loginRequest: LoginRequest): Call<TokenResponse>
}