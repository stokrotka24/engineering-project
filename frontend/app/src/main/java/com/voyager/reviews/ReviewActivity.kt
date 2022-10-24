package com.voyager.reviews

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.Gravity
import android.view.View
import android.widget.PopupMenu
import android.widget.ProgressBar
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.voyager.R
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.api.HttpStatus
import com.voyager.api.hotels.HotelDetails
import com.voyager.api.reviews.ReviewDetails
import com.voyager.api.reviews.ReviewPage
import com.voyager.databinding.ActivityReviewBinding
import retrofit2.Call
import retrofit2.Response

private const val TAG = "ReviewActivity"
private val mapSortType = mapOf(
    -1 to null,
    R.id.starsAsc to "stars",
    R.id.starsDesc to "-stars",
    R.id.dateAsc to "date",
    R.id.dateDesc to "-date"
)

class ReviewActivity : AppCompatActivity() {
    private lateinit var binding: ActivityReviewBinding
    private lateinit var hotel: HotelDetails
    private lateinit var recyclerView: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var reviewAdapter: ReviewAdapter
    private var reviewList: ArrayList<ReviewDetails> = ArrayList()
    private var lytManager: LinearLayoutManager = LinearLayoutManager(this)
    private var sortType: Int = -1
    private var pageOffset: Int = 0
    private var isLastPage: Boolean = false


    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        binding = ActivityReviewBinding.inflate(layoutInflater)
        setContentView(binding.root)
        hotel = intent.getParcelableArrayListExtra<HotelDetails>("hotel")!![0]
        setToolbar()
        setHotelBaseInfo()
        setSorting()

        if (savedInstanceState != null) {
            reviewList =
                savedInstanceState.getParcelableArrayList<ReviewDetails>("reviews") as ArrayList<ReviewDetails>
            lytManager.onRestoreInstanceState(savedInstanceState.getParcelable("lytManager"))
            pageOffset = savedInstanceState.getInt("pageOffset")
            isLastPage = savedInstanceState.getBoolean("isLastPage")
            sortType = savedInstanceState.getInt("sortType", -1)

        }
        progressBar = binding.progressBar
        progressBar.visibility = View.GONE

        reviewAdapter = ReviewAdapter(reviewList)
        recyclerView = binding.reviewRecyclerView
        recyclerView.apply {
            layoutManager = lytManager
            adapter = reviewAdapter
        }
        recyclerView.addOnScrollListener(
            object : RecyclerView.OnScrollListener() {
                override fun onScrolled(recyclerView: RecyclerView, dx: Int, dy: Int) {
                    super.onScrolled(recyclerView, dx, dy)
                    Log.d(TAG, "onScrolled: pageOffset = $pageOffset")
                    Log.d(TAG, "onScrolled: isLastPage = $isLastPage")
                    Log.d(TAG, "onScrolled: lytManager.childCount = ${lytManager.childCount}")
                    Log.d(TAG, "onScrolled: lytManager.itemCount = ${lytManager.itemCount}")
                    Log.d(TAG, "onScrolled: lytManager.findFirstVisibleItemPosition() = ${lytManager.findFirstVisibleItemPosition()}")
                    Log.d(TAG, "onScrolled: lytManager.findLastVisibleItemPosition() = ${lytManager.findLastVisibleItemPosition()}")
                    Log.d(TAG, "onScrolled: lytManager.findLastCompletelyVisibleItemPosition() = ${lytManager.findLastCompletelyVisibleItemPosition()}")

                    // if page isn't last and data isn't being loaded now and user achieved end of available data, load next data
                    if (!isLastPage && progressBar.visibility == View.GONE && lytManager.findLastCompletelyVisibleItemPosition() + 1 == lytManager.itemCount) {
                        pageOffset += 10
                        getReviews()
                    }
                }
            }
        )

        if (reviewList.isEmpty()) {
            getReviews()
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        Log.d(TAG, "onSaveInstanceState")
        outState.putParcelableArrayList("reviews", reviewList)
        outState.putParcelable("lytManager", lytManager.onSaveInstanceState())
        outState.putInt("pageOffset", pageOffset)
        outState.putBoolean("isLastPage", isLastPage)
        outState.putInt("sortType", sortType)
        super.onSaveInstanceState(outState)
    }

    private fun setToolbar() {
        val toolbar = binding.returnToolbar
        toolbar.title = hotel.name
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setDisplayShowHomeEnabled(true)
        toolbar.setNavigationOnClickListener { onBackPressed() }
    }

    private fun setHotelBaseInfo() {
        binding.rating.text = hotel.stars
        binding.reviewCount.text = hotel.review_count.toString()
    }

    private fun setSorting() {
        val sortBtn = binding.sortBtn
        val sortMenu = PopupMenu(this, sortBtn, Gravity.END)
        sortMenu.menuInflater.inflate(R.menu.sort_reviews_menu, sortMenu.menu)
        if (sortType >= 0) {
            sortMenu.menu.findItem(sortType).isChecked = true
        }
        sortMenu.setOnMenuItemClickListener { item ->
            Log.d(TAG, "setOnMenuItemClickListener: ")
            item.isChecked = true
            sortType = item.itemId
            Log.d(TAG, "setSorting: $sortType")
            Log.d(TAG, "setSorting: ${
                mapSortType[sortType]}")

            pageOffset = 0
            isLastPage = false
            reviewList.clear()
            getReviews()

            reviewAdapter.notifyDataSetChanged()
            true
        }
        sortBtn.setOnClickListener {
            sortMenu.show()
        }
    }


    private fun getReviews() {
        progressBar.visibility = View.VISIBLE

        val api = ApiUtils.getApi()
        val getReviewDetailsCall: Call<ReviewPage> = api.getReviewDetails(hotel.id, mapSortType[sortType], pageOffset)
        getReviewDetailsCall.enqueue(object : DefaultCallback<ReviewPage?>(this) {
            override fun onSuccess(response: Response<ReviewPage?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        val responseBody = response.body()!!
                        val reviews = responseBody.results
                        reviewList.addAll(reviews)
                        reviewAdapter.notifyDataSetChanged()
                        if (responseBody.next == null) {
                            isLastPage = true
                        }
                        Log.d(TAG, "onSuccess: isLastPage = $isLastPage")

                        progressBar.visibility = View.GONE
                    }
                }
            }
        })
    }
}