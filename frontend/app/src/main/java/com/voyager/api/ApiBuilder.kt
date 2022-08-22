package com.voyager.api

import com.voyager.BuildConfig
import okhttp3.OkHttpClient
import retrofit2.Converter
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class ApiBuilder<T : Any>{
    private val converterFactory: Converter.Factory = GsonConverterFactory.create()
    private val baseUrl: String = BuildConfig.API_URL

    private lateinit var client: OkHttpClient
    private lateinit var service: Class<T>

    fun client(client: OkHttpClient) = apply { this.client = client }

    fun service(service: Class<T>) = apply { this.service = service }

    fun build(): T {
        return Retrofit.Builder()
            .addConverterFactory(converterFactory)
            .baseUrl(baseUrl)
            .client(client)
            .build()
            .create(service)
    }
}