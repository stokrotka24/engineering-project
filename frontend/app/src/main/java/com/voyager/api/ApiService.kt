package com.voyager.api
import com.voyager.api.hotels.Hotel
import com.voyager.api.hotels.HotelDetails
import com.voyager.api.reviews.HotelReview
import com.voyager.api.reviews.Review
import com.voyager.api.reviews.UserReview
import com.voyager.api.tokens.TokenResponse
import com.voyager.api.user.*
import retrofit2.Call
import retrofit2.http.*

/**
 * Interface with definitions of API calls
 */
interface ApiService {
    @POST("register/")
    fun register(@Body registerRequest: RegisterRequest): Call<RegisterResponse>

    @POST("login/")
    fun login(@Body loginRequest: LoginRequest): Call<TokenResponse>

    /**
     * Creates call with change password request.
     *
     * @param id id of the user, who wants to change password
     * @param changePassRequest contains old password, new password and new password confirmation
     */
    @PUT("change_password/{id}")
    fun changePassword(@Path("id") id: Int, @Body changePassRequest: ChangePassRequest): Call<ChangePassResponse>

    @GET("account_info/")
    fun getAccountInfo(): Call<UserAccount>

    /**
     * Creates call with request to get hotel recommendations.
     *
     * @param noRecommendations number of hotel recommendations user wants to get
     */
    @GET("hotels/")
    fun getHotels(@Query("no_recommendations") noRecommendations: Int): Call<List<Hotel>>

    /**
     * Creates call with request to get hotel recommendations from certain city.
     *
     * @param city city from which user wants to get hotel recommendations
     * @param noRecommendations number of hotel recommendations user wants to get
     */
    @GET("hotels/")
    fun getHotels(@Query("city") city: String, @Query("no_recommendations") noRecommendations: Int): Call<List<Hotel>>

    /**
     * Creates call with request to get detailed information about hotel.
     *
     * @param id id of the hotel whose details user requested
     */
    @GET("hotels/{id}")
    fun getHotelDetails(@Path("id") id: Int): Call<HotelDetails>

    @POST("create_review/")
    fun createReview(@Body review: Review): Call<Review>

    /**
     * Creates call with request to get reviews for given hotel.
     *
     * @param hotelId id of the hotel whose reviews user requested
     * @param sortType the way the reviews are sorted
     * @param offset which review will be sent as first
     * @param limit how many reviews will be sent
     */
    @GET("hotel_reviews/")
    fun getHotelReviews(@Query("hotel_id") hotelId: Int, @Query("sort_type") sortType: String?, @Query("offset") offset: Int, @Query("limit") limit: Int = 10): Call<Page<HotelReview>>

    @GET("user_reviews/")
    fun getUserReviews(@Query("sort_type") sortType: String?, @Query("offset") offset: Int, @Query("limit") limit: Int = 10): Call<Page<UserReview>>

    @DELETE("delete_review/{id}")
    fun deleteReview(@Path("id") id:Int): Call<Unit>
}