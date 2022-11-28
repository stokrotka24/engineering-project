package com.voyager.api.tokens

import android.content.Context
import android.util.Log
import com.voyager.api.ApiUtils
import okhttp3.Interceptor
import okhttp3.Response

private const val TAG = "TokenInterceptor"

class TokenInterceptor(context: Context): Interceptor {
    private val tokenManager = TokenManager(context)

    /**
     * Add access token to request header.
     *
     * @param chain contains request to be sent
     * @return chain with request with attached access token
     */
    override fun intercept(chain: Interceptor.Chain): Response {
        Log.d(TAG, "intercept: ")

        val requestBuilder = chain.request().newBuilder()
        tokenManager.getAccessToken()?.let {
            requestBuilder.addHeader(ApiUtils.AUTHORIZATION_HEADER, "Bearer $it")
        }
        return chain.proceed(requestBuilder.build())
    }
}