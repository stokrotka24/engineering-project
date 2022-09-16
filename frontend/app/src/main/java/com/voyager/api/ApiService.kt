package com.voyager.api
import com.voyager.api.hotels.Hotel
import com.voyager.api.login.LoginRequest
import com.voyager.api.registration.RegisterRequest
import com.voyager.api.registration.RegisterResponse
import com.voyager.api.tokens.TokenResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

interface ApiService {
    @POST("register/")
    fun register(@Body registerRequest: RegisterRequest): Call<RegisterResponse>

    @POST("login/")
    fun login(@Body loginRequest: LoginRequest): Call<TokenResponse>

    @GET("hotels/")
    fun getHotels(@Query("no_recommendations") noRecommendations: Int): Call<List<Hotel>>

    @GET("hotels/")
    fun getHotels(@Query("city") city: String, @Query("no_recommendations") noRecommendations: Int): Call<List<Hotel>>
}