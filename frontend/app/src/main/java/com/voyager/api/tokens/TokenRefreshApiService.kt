package com.voyager.api.tokens

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface TokenRefreshApiService {
    @POST("login/refresh/")
    fun tokenRefresh(@Body tokenRefreshRequest: TokenRefreshRequest): Call<TokenResponse>
}