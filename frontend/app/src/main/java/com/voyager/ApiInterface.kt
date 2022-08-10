package com.voyager

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiInterface {
    @GET("hello/")
    fun postHello(): Call<ServerHello>

    @POST("hello/")
    fun postHello(@Body clientHello: ClientHello): Call<ServerHello>
}