package com.voyager.api

import com.voyager.BuildConfig
import okhttp3.OkHttpClient
import retrofit2.Converter
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

/**
 * Builds Retrofit instance with given client and service.
 *
 * @param <T> interface with defined HTTP requests
 */
class ApiBuilder<T : Any>{
    private val converterFactory: Converter.Factory = GsonConverterFactory.create()
    private val baseUrl: String = BuildConfig.API_URL

    private lateinit var client: OkHttpClient
    private lateinit var service: Class<T>

    /**
     * @param client if it is logged in client, it includes authenticator and interceptor
     */
    fun client(client: OkHttpClient) = apply { this.client = client }

    /**
     * @param service Class instance (::class.java) created from interface T
     */
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