package com.voyager.hotels

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.android.flexbox.FlexDirection
import com.voyager.R
import com.voyager.api.hotels.HotelDetails
import com.voyager.databinding.ActivityHotelDetailsBinding
import com.google.android.flexbox.FlexboxLayoutManager
import com.google.android.flexbox.JustifyContent
import com.voyager.api.*
import com.voyager.api.hotels.Attribute
import com.voyager.api.reviews.Review
import com.voyager.api.reviews.HotelReview
import com.voyager.reviews.HotelReviewsActivity
import com.voyager.reviews.HotelReviewAdapter
import retrofit2.Call
import retrofit2.Response


private const val TAG = "HotelDetailsActivity"
private const val MAX_LEN_REVIEW = 5000
private const val MAX_NUM_REVIEW = 2

class HotelDetailsActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHotelDetailsBinding
    private lateinit var api: ApiService
    private var hotelId: Int = 0
    private var categoriesList: ArrayList<String> = ArrayList()
    private lateinit var categoryAdapter: CategoryAdapter
    private var attributesList: ArrayList<Attribute> = ArrayList()
    private lateinit var attributeAdapter: AttributeAdapter
    private var reviewsList: ArrayList<HotelReview> = ArrayList()
    private lateinit var reviewAdapter: HotelReviewAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        binding = ActivityHotelDetailsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setToolbar()
        setCategoriesRecyclerView()
        setAttributesRecyclerView()
        setReviewsRecyclerView()

        api = ApiUtils.getApi()
        hotelId = intent.getIntExtra("hotelId", 0)
        binding.hotel = HotelDetails(0, getString(R.string.hotel_name),
            getString(R.string.value_not_loaded), getString(R.string.value_not_loaded),
            "", "",0F, 0, ArrayList(), ArrayList())
        fetchHotel(createView=true)
        fetchReviews()
    }

    private fun setToolbar() {
        val toolbar = binding.returnToolbar
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setDisplayShowHomeEnabled(true)
        toolbar.setNavigationOnClickListener { onBackPressed() }
    }

    override fun onBackPressed() {
        val intent = Intent()
        intent.putExtra("hotel", binding.hotel)
        setResult(Activity.RESULT_OK, intent)
        super.onBackPressed()
    }

    private fun setCategoriesRecyclerView() {
        val categoryManager = FlexboxLayoutManager(this)
        categoryManager.flexDirection = FlexDirection.ROW
        categoryManager.justifyContent = JustifyContent.FLEX_START
        categoryAdapter = CategoryAdapter(categoriesList)
        binding.categoryRecyclerView.apply {
            layoutManager = categoryManager
            adapter = categoryAdapter
        }
    }

    private fun setAttributesRecyclerView() {
        val attributeManager = FlexboxLayoutManager(this)
        attributeManager.flexDirection = FlexDirection.ROW
        attributeManager.justifyContent = JustifyContent.FLEX_START
        attributeAdapter = AttributeAdapter(this, attributesList)
        binding.attributesRecyclerView.apply {
            layoutManager = attributeManager
            adapter = attributeAdapter
        }
    }

    private fun setReviewsRecyclerView() {
        reviewAdapter = HotelReviewAdapter(reviewsList)
        binding.reviewRecyclerView.apply {
            layoutManager = LinearLayoutManager(applicationContext)
            adapter = reviewAdapter
        }
    }

    private fun fetchHotel(createView: Boolean=false) {
        binding.progressBar.visibility = View.VISIBLE

        val getHotelDetailsCall: Call<HotelDetails> = api.getHotelDetails(hotelId)
        getHotelDetailsCall.enqueue(object : DefaultCallback<HotelDetails?>(this) {
            override fun onSuccess(response: Response<HotelDetails?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        binding.hotel = response.body()!!
                        if (createView) { createView() }
                        binding.progressBar.visibility = View.GONE
                    }
                }
            }
        })
    }

    private fun createView() {
        categoriesList.addAll(binding.hotel!!.categories)
        categoryAdapter.notifyItemRangeInserted(0,  categoriesList.size)

        binding.hotel!!.attributes?.let {
            attributesList.addAll(it)
            attributeAdapter.notifyItemRangeInserted(0, attributesList.size)
        }

        binding.submitReviewButton.setOnClickListener { submitReviewButtonClicked() }
        binding.seeAllReviewsButton.setOnClickListener { seeAllReviewsButtonClicked() }
    }


    private fun fetchReviews() {
        val getReviewsCall: Call<Page<HotelReview>> = api.getHotelReviews(hotelId, "-date", 0, MAX_NUM_REVIEW)
        getReviewsCall.enqueue(object : DefaultCallback<Page<HotelReview>?>(this) {
            override fun onSuccess(response: Response<Page<HotelReview>?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        val reviews = response.body()!!.results
                        reviewsList.clear()

                        if (reviews.isEmpty()) {
                            binding.noReviewsTextView.visibility = View.VISIBLE
                            binding.seeAllReviewsButton.visibility = View.GONE
                        } else {
                            binding.noReviewsTextView.visibility = View.GONE
                            binding.seeAllReviewsButton.visibility = View.VISIBLE
                            reviewsList.addAll(reviews)
                        }
                        reviewAdapter.notifyDataSetChanged()
                    }
                }
            }
        })
    }

    private fun submitReviewButtonClicked() {
        Log.d(TAG, "submitReviewButtonClicked: ")
        val stars = binding.ratingBar.rating.toInt()
        val reviewContent = binding.reviewContent.text.toString()

        if (stars == 0) {
            Toast.makeText(this, "You have to select number of stars", Toast.LENGTH_LONG).show()
        } else if (reviewContent.length > MAX_LEN_REVIEW) {
            Toast.makeText(this, "Your review has more than $MAX_LEN_REVIEW characters. Shorten it, please", Toast.LENGTH_LONG).show()
        } else {
            val review = Review(null, hotelId, stars, reviewContent)

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
                            fetchHotel()
                        }
                        else -> {
                            Toast.makeText(applicationContext, getString(R.string.server_error), Toast.LENGTH_LONG).show()
                        }
                    }
                }
            })
        }
    }

    private fun seeAllReviewsButtonClicked() {
        Log.d(TAG, "seeAllReviewsButtonClicked: ")
        val intent = Intent(this, HotelReviewsActivity::class.java)
        intent.putExtra("hotel", binding.hotel)
        startActivity(intent)
    }
}