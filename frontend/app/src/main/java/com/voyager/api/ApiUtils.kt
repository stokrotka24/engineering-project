package com.voyager.api

import android.content.Context
import android.util.Log
import com.voyager.api.tokens.TokenAuthenticator
import com.voyager.api.tokens.TokenInterceptor
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

    fun loggedIn(context: Context) {
        Log.d(TAG, "loggedIn: ")

        val loggedClient = OkHttpClient.Builder()
            .addInterceptor(TokenInterceptor(context))
            .authenticator(TokenAuthenticator(context))
            .build()
        api = apiBuilder
            .client(loggedClient)
            .build()
    }

    fun loggedOut() {
        Log.d(TAG, "loggedOut: ")

        api = apiBuilder
            .client(client)
            .build()
    }

    fun getApi(): ApiService {
        return api
    }
}