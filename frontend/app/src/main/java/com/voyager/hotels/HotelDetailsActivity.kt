package com.voyager.hotels

import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.flexbox.FlexDirection
import com.voyager.R
import com.voyager.api.hotels.HotelDetails
import com.voyager.databinding.ActivityHotelDetailsBinding
import com.google.android.flexbox.FlexboxLayoutManager
import com.google.android.flexbox.JustifyContent
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.api.HttpStatus
import com.voyager.api.hotels.Attribute
import com.voyager.api.hotels.Review
import retrofit2.Call
import retrofit2.Response


private const val TAG = "HotelDetailsActivity"
private const val MAX_REVIEW_LEN = 5000

class HotelDetailsActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHotelDetailsBinding
    private lateinit var hotel: HotelDetails

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        binding = ActivityHotelDetailsBinding.inflate(layoutInflater)
        binding.submitReviewButton.setOnClickListener { submitReviewButtonClicked() }
        setContentView(binding.root)
        hotel = intent.getParcelableArrayListExtra<HotelDetails>("hotel")!![0]

        binding.name.text = hotel.name
        binding.rating.text = hotel.stars
        binding.reviewCount.text = hotel.review_count.toString()
        binding.street.text = hotel.address
        binding.cityState.text =
            getString(R.string.cityState, hotel.city, hotel.state, hotel.postal_code)
    }

    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()

        val categoryManager = FlexboxLayoutManager(this)
        categoryManager.flexDirection = FlexDirection.ROW
        categoryManager.justifyContent = JustifyContent.FLEX_START
        val categoryAdapter = CategoryAdapter(hotel.categories as ArrayList<String>)
        binding.categoryRecyclerView.apply {
            layoutManager = categoryManager
            adapter = categoryAdapter
        }
        categoryAdapter.notifyDataSetChanged()

        val attributeManager = FlexboxLayoutManager(this)
        attributeManager.flexDirection = FlexDirection.ROW
        attributeManager.justifyContent = JustifyContent.FLEX_START
        val attributeAdapter =
            AttributeAdapter(applicationContext, hotel.attributes as ArrayList<Attribute>)
        binding.attributesRecyclerView.apply {
            layoutManager = attributeManager
            adapter = attributeAdapter
        }
        attributeAdapter.notifyDataSetChanged()
    }

    private fun submitReviewButtonClicked() {
        Log.d(TAG, "submitReviewButtonClicked: ")
        val stars = binding.ratingBar.rating.toInt()
        val reviewContent = binding.reviewContent.text.toString()
        if (stars == 0) {
            Toast.makeText(this, "You have to select number of stars", Toast.LENGTH_LONG).show()
        } else if (reviewContent.length > MAX_REVIEW_LEN) {
            Toast.makeText(this, "Your review has more than $MAX_REVIEW_LEN characters. Shorten it, please", Toast.LENGTH_LONG).show()
        } else {
            val api = ApiUtils.getApi()
            val review = Review(null, hotel.id, stars, reviewContent)
            val createReviewCall: Call<Review> = api.createReview(review)
            createReviewCall.enqueue(object : DefaultCallback<Review?>(this) {
                override fun onSuccess(response: Response<Review?>) {
                    val responseCode = response.code()
                    Log.d(TAG, "onSuccess: response.code = $responseCode")

                    when (responseCode) {
                        HttpStatus.Created.code -> {
                            Toast.makeText(applicationContext, "Thank you for leaving your review!", Toast.LENGTH_LONG).show()
                            binding.ratingBar.rating = 0F
                            binding.reviewContent.text.clear()
                        }
                        else -> {
                            Toast.makeText(applicationContext, getString(R.string.server_error), Toast.LENGTH_LONG).show()
                        }
                    }
                }
            })
        }
    }
}