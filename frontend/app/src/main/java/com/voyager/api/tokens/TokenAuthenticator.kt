package com.voyager.api.tokens

import android.content.Context
import android.util.Log
import com.voyager.api.ApiBuilder
import com.voyager.api.ApiUtils
import com.voyager.api.HttpStatus
import okhttp3.*

private const val TAG = "TokenAuthenticator"

class TokenAuthenticator(context: Context): Authenticator {
    private val tokenManager = TokenManager(context)
    private val tokenRefreshApi = buildTokenRefreshApi()

    private fun buildTokenRefreshApi(): TokenRefreshApiService {
        Log.d(TAG, "buildTokenRefreshApi: ")

        val client: OkHttpClient = OkHttpClient.Builder().build()
        return ApiBuilder<TokenRefreshApiService>()
                .client(client)
                .service(TokenRefreshApiService::class.java)
                .build()
    }

    override fun authenticate(route: Route?, response: Response): Request? {
        Log.d(TAG, "authenticate: ")

        return try {
            val renewedAccessToken = getRenewedAccessToken()
            response.request().newBuilder()
                .header(ApiUtils.AUTHORIZATION_HEADER, "Bearer $renewedAccessToken")
                .build()
        } catch (ex: RefreshTokenExpiredException) {
            tokenManager.removeTokens()
            ApiUtils.loggedOut()
            null
        }
    }

    private fun getRenewedAccessToken(): String {
        Log.d(TAG, "getRenewedAccessToken: ")
        val refreshTokenRequest = TokenRefreshRequest(tokenManager.getRefreshToken())
        val response = tokenRefreshApi.tokenRefresh(refreshTokenRequest).execute()

        if (response.code() == HttpStatus.Unauthorized.code) {
            throw RefreshTokenExpiredException()
        }

        val tokenResponse = response.body()!!
        tokenManager.saveTokens(tokenResponse.access, tokenResponse.refresh)
        return tokenResponse.access
    }
}