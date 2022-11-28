package com.voyager.api.tokens

import android.content.Context
import android.content.SharedPreferences
import com.voyager.R

/**
 * Manages access to access and refresh tokens.
 *
 * @param context application context needed to use shared preferences
 */
class TokenManager(context: Context) {
    private val preferences: SharedPreferences = context.getSharedPreferences(context.getString(R.string.app_name), Context.MODE_PRIVATE)
    companion object {
        private const val ACCESS_TOKEN = "access_token"
        private const val REFRESH_TOKEN = "refresh_token"
    }

    fun saveTokens(accessToken: String, refreshToken: String) {
        val editor = preferences.edit()
        editor.putString(ACCESS_TOKEN, accessToken)
        editor.putString(REFRESH_TOKEN, refreshToken)
        editor.apply()
    }

    fun removeTokens() {
        val editor = preferences.edit()
        editor.remove(ACCESS_TOKEN)
        editor.remove(REFRESH_TOKEN)
        editor.apply()
    }

    fun getAccessToken(): String? {
        return preferences.getString(ACCESS_TOKEN, null)
    }

    fun getRefreshToken(): String? {
        return preferences.getString(REFRESH_TOKEN, null)
    }
}