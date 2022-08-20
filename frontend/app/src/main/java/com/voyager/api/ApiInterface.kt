package com.voyager.api

import com.voyager.*
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiInterface {
    @GET("hello/")
    fun getHello(): Call<ServerHello>

    @POST("hello/")
    fun postHello(@Body clientHello: ClientHello): Call<ServerHello>

    @POST("register/")
    fun register(@Body registerRequest: RegisterRequest): Call<RegisterResponse>

    @POST("login/")
    fun login(@Body loginRequest: LoginRequest): Call<LoginResponse>
}