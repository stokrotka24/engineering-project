package com.voyager.hotels

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat.startActivity
import androidx.recyclerview.widget.LinearLayoutManager
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
import com.voyager.api.reviews.Review
import com.voyager.api.reviews.ReviewDetails
import com.voyager.api.reviews.ReviewPage
import com.voyager.reviews.ReviewActivity
import com.voyager.reviews.ReviewAdapter
import retrofit2.Call
import retrofit2.Response


private const val TAG = "HotelDetailsActivity"
private const val MAX_REVIEW_LEN = 5000
private const val MAX_REVIEW_NUM = 2

class HotelDetailsActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHotelDetailsBinding
    private lateinit var hotel: HotelDetails

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        binding = ActivityHotelDetailsBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setToolbar()
        binding.submitReviewButton.setOnClickListener { submitReviewButtonClicked() }
        binding.seeAllReviewsButton.setOnClickListener { seeAllReviewsButtonClicked() }
        hotel = intent.getParcelableArrayListExtra<HotelDetails>("hotel")!![0]

        setHotelBaseInfo()
        setCategories()
        setAttributes()
        setReviews()
    }

    private fun setToolbar() {
        val toolbar = binding.returnToolbar
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setDisplayShowHomeEnabled(true)
        toolbar.setNavigationOnClickListener { onBackPressed() }
    }

    private fun setHotelBaseInfo() {
        binding.name.text = hotel.name
        binding.rating.text = hotel.stars
        binding.reviewCount.text = hotel.review_count.toString()
        binding.street.text = hotel.address
        binding.cityState.text =
            getString(R.string.cityState, hotel.city, hotel.state, hotel.postal_code)
    }

    private fun setCategories() {
        val categoryManager = FlexboxLayoutManager(this)
        categoryManager.flexDirection = FlexDirection.ROW
        categoryManager.justifyContent = JustifyContent.FLEX_START
        val categoryAdapter = CategoryAdapter(hotel.categories as ArrayList<String>)
        binding.categoryRecyclerView.apply {
            layoutManager = categoryManager
            adapter = categoryAdapter
        }
        categoryAdapter.notifyDataSetChanged()
    }

    private fun setAttributes() {
        if (hotel.attributes != null) {
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
    }

    private fun setReviews(reviews: List<ReviewDetails>) {
        val reviewManager = LinearLayoutManager(this)
        val reviewAdapter = ReviewAdapter(reviews as ArrayList<ReviewDetails>)
        binding.reviewRecyclerView.apply {
            layoutManager = reviewManager
            adapter = reviewAdapter
        }
        reviewAdapter.notifyDataSetChanged()
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

    private fun setReviews() {
        val api = ApiUtils.getApi()
        val getReviewDetailsCall: Call<ReviewPage> = api.getReviewDetails(hotel.id, null, 0, MAX_REVIEW_NUM)
        getReviewDetailsCall.enqueue(object : DefaultCallback<ReviewPage?>(this) {
            override fun onSuccess(response: Response<ReviewPage?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        val reviews = response.body()!!.results

                        if (reviews.isEmpty()) {
                            binding.noReviewsTextView.visibility = View.VISIBLE
                            binding.seeAllReviewsButton.visibility = View.GONE
                        } else {
                            binding.noReviewsTextView.visibility = View.GONE
                            binding.seeAllReviewsButton.visibility = View.VISIBLE
                            setReviews(reviews)
                        }
                    }
                }
            }
        })
    }

    private fun seeAllReviewsButtonClicked() {
        Log.d(TAG, "seeAllReviewsButtonClicked: ")
        val intent = Intent(this, ReviewActivity::class.java)
        // TODO put as object not as an array
        intent.putParcelableArrayListExtra("hotel", arrayListOf(hotel))
        startActivity(intent)
    }
}