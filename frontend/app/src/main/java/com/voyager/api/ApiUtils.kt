package com.voyager.api

import android.content.Context
import android.util.Log
import com.voyager.api.tokens.TokenAuthenticator
import com.voyager.api.tokens.TokenInterceptor
import com.voyager.api.tokens.TokenManager
import com.voyager.api.tokens.TokenResponse
import okhttp3.OkHttpClient

private const val TAG = "ApiUtils"

object ApiUtils {
    private val apiBuilder = ApiBuilder<ApiService>()
    private val client: OkHttpClient = OkHttpClient.Builder().build()
    private var api: ApiService

    const val AUTHORIZATION_HEADER = "Authorization"

    init {
        Log.d(TAG, "init: ")

        api = apiBuilder
            .client(client)
            .service(ApiService::class.java)
            .build()
    }

    fun loggedIn(context: Context, tokenResponse: TokenResponse) {
        Log.d(TAG, "loggedIn: ")
        TokenManager(context).saveTokens(tokenResponse.access, tokenResponse.refresh)


        val loggedClient = OkHttpClient.Builder()
            .addInterceptor(TokenInterceptor(context))
            .authenticator(TokenAuthenticator(context))
            .build()
        api = apiBuilder
            .client(loggedClient)
            .build()
    }

    fun loggedOut(context: Context) {
        Log.d(TAG, "loggedOut: ")
        TokenManager(context).removeTokens()

        api = apiBuilder
            .client(client)
            .build()
    }

    fun getApi(): ApiService {
        return api
    }
}