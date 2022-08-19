package com.voyager.api

import android.util.Log
import com.voyager.BuildConfig
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

private const val TAG = "ApiService"

object ApiService {
    private val okHttpClient: OkHttpClient = OkHttpClient().newBuilder().build()
    private val api: ApiInterface = buildApi()

    private fun buildApi(): ApiInterface {
        Log.d(TAG, "buildApi: ")
        return Retrofit.Builder()
            .addConverterFactory(GsonConverterFactory.create())
            .baseUrl(BuildConfig.API_URL)
            .client(okHttpClient)
            .build()
            .create(ApiInterface::class.java)
    }

    fun getApi(): ApiInterface {
        return api
    }
}