package com.voyager.api.tokens

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface TokenRefreshApiService {
    /**
     * Creates call to API with request containing refresh token in order to renew access token.
     */
    @POST("login/refresh/")
    fun tokenRefresh(@Body tokenRefreshRequest: TokenRefreshRequest): Call<TokenResponse>
}