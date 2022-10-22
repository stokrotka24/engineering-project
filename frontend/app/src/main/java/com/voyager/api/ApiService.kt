package com.voyager.api
import com.voyager.api.hotels.Hotel
import com.voyager.api.hotels.HotelDetails
import com.voyager.api.hotels.Review
import com.voyager.api.login.LoginRequest
import com.voyager.api.registration.RegisterRequest
import com.voyager.api.registration.RegisterResponse
import com.voyager.api.tokens.TokenResponse
import retrofit2.Call
import retrofit2.http.*

interface ApiService {
    @POST("register/")
    fun register(@Body registerRequest: RegisterRequest): Call<RegisterResponse>

    @POST("login/")
    fun login(@Body loginRequest: LoginRequest): Call<TokenResponse>

    @GET("hotels/")
    fun getHotels(@Query("no_recommendations") noRecommendations: Int): Call<List<Hotel>>

    @GET("hotels/")
    fun getHotels(@Query("city") city: String, @Query("no_recommendations") noRecommendations: Int): Call<List<Hotel>>

    @GET("hotels/{id}")
    fun getHotelDetails(@Path("id") id: Int): Call<HotelDetails>

    @POST("create_review")
    fun createReview(@Body review: Review): Call<Review>
}