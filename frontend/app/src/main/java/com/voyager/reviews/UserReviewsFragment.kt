package com.voyager.reviews

import android.app.AlertDialog
import android.os.Bundle
import android.util.Log
import android.view.Gravity
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.PopupMenu
import android.widget.ProgressBar
import android.widget.Toast
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.voyager.R
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.api.HttpStatus
import com.voyager.api.Page
import com.voyager.api.reviews.UserReview
import retrofit2.Call
import retrofit2.Response

private const val TAG = "UserReviewsFragment"

class UserReviewsFragment : Fragment(), UserReviewAdapter.OnLongClickListener {
    private lateinit var recyclerView: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var reviewAdapter: UserReviewAdapter
    private var reviewList: ArrayList<UserReview> = ArrayList()
    private var lytManager: LinearLayoutManager = LinearLayoutManager(context)
    private var sortType: Int = R.id.dateDesc
    private var pageOffset: Int = 0
    private var isLastPage: Boolean = false

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        Log.d(TAG, "onCreateView: ")
        return inflater.inflate(R.layout.fragment_user_reviews, container, false)
    }

    override fun onViewStateRestored(savedInstanceState: Bundle?) {
        Log.d(TAG, "onViewStateRestored: ")
        super.onViewStateRestored(savedInstanceState)

        if (savedInstanceState != null) {
            reviewList =
                savedInstanceState.getParcelableArrayList<UserReview>("reviews") as ArrayList<UserReview>
            lytManager.onRestoreInstanceState(savedInstanceState.getParcelable("lytManager"))
            pageOffset = savedInstanceState.getInt("pageOffset")
            isLastPage = savedInstanceState.getBoolean("isLastPage")
            sortType = savedInstanceState.getInt("sortType", -1)
        }

    }

    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()

        setSorting()

        progressBar = view?.findViewById(R.id.progressBar)!!
        progressBar.visibility = View.GONE
        reviewAdapter = UserReviewAdapter(reviewList, this)
        recyclerView = view?.findViewById(R.id.reviewRecyclerView)!!
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

    private fun setSorting() {
        val sortBtn = view?.findViewById<Button>(R.id.sortBtn)!!
        val sortMenu = PopupMenu(context, sortBtn, Gravity.END)
        sortMenu.menuInflater.inflate(R.menu.sort_reviews_menu, sortMenu.menu)
        sortMenu.menu.findItem(sortType).isChecked = true
        sortMenu.setOnMenuItemClickListener { item ->
            Log.d(TAG, "setOnMenuItemClickListener: ")
            item.isChecked = true
            sortType = item.itemId
            Log.d(TAG, "setSorting: $sortType")
            Log.d(TAG, "setSorting: ${mapSortType[sortType]}")

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
            val getReviewDetailsCall: Call<Page<UserReview>> = api.getUserReviews(mapSortType[sortType], pageOffset)
            getReviewDetailsCall.enqueue(object : DefaultCallback<Page<UserReview>?>(requireContext()) {
            override fun onSuccess(response: Response<Page<UserReview>?>) {
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

    /**
     * This method is invoked when review from list is long clicked.
     * Deletes selected review, if it is confirmed in displayed dialog.
     *
     * @param review long clicked review
     */
    override fun onItemLongClicked(review: UserReview): Boolean {
        val dialogBuilder = AlertDialog.Builder(context)
        dialogBuilder
            .setMessage("Are you sure you want to delete this review?")
            .setPositiveButton("YES") { _, _ -> removeReview(review) }
            .setNegativeButton("NO", null)

        val dialog = dialogBuilder.create()
        dialog.show()

        return true
    }

    private fun removeReview(review: UserReview) {
        val api = ApiUtils.getApi()
        val deleteReviewCall: Call<Unit> = api.deleteReview(review.id)
        deleteReviewCall.enqueue(object : DefaultCallback<Unit?>(requireContext()) {
            override fun onSuccess(response: Response<Unit?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.NoContent.code -> {
                        reviewList.remove(review)
                        reviewAdapter.notifyDataSetChanged()
                        Toast.makeText(context, "Review has been deleted", Toast.LENGTH_LONG).show()
                    } else -> {
                        Toast.makeText(context, getString(R.string.server_error), Toast.LENGTH_LONG).show()
                    }
                }
            }
        })
    }
}