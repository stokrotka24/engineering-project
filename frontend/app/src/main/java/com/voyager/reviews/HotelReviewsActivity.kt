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
import com.voyager.api.reviews.HotelReview
import com.voyager.api.Page
import com.voyager.databinding.ActivityHotelReviewsBinding
import retrofit2.Call
import retrofit2.Response

private const val TAG = "ReviewActivity"
val mapSortType = mapOf(
    R.id.starsAsc to "stars",
    R.id.starsDesc to "-stars",
    R.id.dateAsc to "date",
    R.id.dateDesc to "-date"
)

class HotelReviewsActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHotelReviewsBinding
    private lateinit var hotel: HotelDetails
    private lateinit var recyclerView: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var reviewAdapter: HotelReviewAdapter
    private var reviewList: ArrayList<HotelReview> = ArrayList()
    private var lytManager: LinearLayoutManager = LinearLayoutManager(this)
    private var sortType: Int = R.id.dateDesc
    private var pageOffset: Int = 0
    private var isLastPage: Boolean = false


    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        binding = ActivityHotelReviewsBinding.inflate(layoutInflater)
        setContentView(binding.root)
        hotel = intent.getParcelableExtra("hotel")!!
        setToolbar()
        setHotelBaseInfo()
        setSorting()

        if (savedInstanceState != null) {
            reviewList =
                savedInstanceState.getParcelableArrayList<HotelReview>("reviews") as ArrayList<HotelReview>
            lytManager.onRestoreInstanceState(savedInstanceState.getParcelable("lytManager"))
            pageOffset = savedInstanceState.getInt("pageOffset")
            isLastPage = savedInstanceState.getBoolean("isLastPage")
            sortType = savedInstanceState.getInt("sortType", -1)

        }
        progressBar = binding.progressBar
        progressBar.visibility = View.GONE

        reviewAdapter = HotelReviewAdapter(reviewList)
        recyclerView = binding.reviewRecyclerView
        recyclerView.apply {
            layoutManager = lytManager
            adapter = reviewAdapter
        }
        recyclerView.addOnScrollListener(
            object : RecyclerView.OnScrollListener() {
                override fun onScrolled(recyclerView: RecyclerView, dx: Int, dy: Int) {
                    super.onScrolled(recyclerView, dx, dy)
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
        toolbar.title = "Reviews for ${hotel.name}"
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setDisplayShowHomeEnabled(true)
        toolbar.setNavigationOnClickListener { onBackPressed() }
    }

    private fun setHotelBaseInfo() {
        binding.rating.text = hotel.stars.toString()
        binding.reviewCount.text = hotel.review_count.toString()
    }

    private fun setSorting() {
        val sortBtn = binding.sortBtn
        val sortMenu = PopupMenu(this, sortBtn, Gravity.END)
        sortMenu.menuInflater.inflate(R.menu.sort_reviews_menu, sortMenu.menu)
        sortMenu.menu.findItem(sortType).isChecked = true
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
        val getReviewsCall: Call<Page<HotelReview>> = api.getHotelReviews(hotel.id, mapSortType[sortType], pageOffset)
        getReviewsCall.enqueue(object : DefaultCallback<Page<HotelReview>?>(this) {
            override fun onSuccess(response: Response<Page<HotelReview>?>) {
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