package com.voyager

import android.annotation.SuppressLint
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ProgressBar
import androidx.recyclerview.widget.LinearLayoutManager
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.api.HttpStatus
import com.voyager.api.hotels.Hotel
import com.voyager.api.hotels.HotelPage
import retrofit2.Call
import retrofit2.Response

private const val TAG = "HotelFragment"

class HotelFragment : Fragment() {
    private lateinit var recyclerView: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var hotelAdapter: HotelAdapter
    private var hotelList: ArrayList<Hotel> = ArrayList()
    private lateinit var lytManager: LinearLayoutManager
    private lateinit var api: ApiService
    private var pageOffset: Int = 0
    private var isLastPage: Boolean = false

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        api = ApiUtils.getApi()
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        Log.d(TAG, "onCreateView: ")
        return inflater.inflate(R.layout.fragment_hotel, container, false)
    }

    override fun onViewStateRestored(savedInstanceState: Bundle?) {
        Log.d(TAG, "onViewStateRestored: ")
        super.onViewStateRestored(savedInstanceState)

        lytManager = LinearLayoutManager(view?.context)

        if (savedInstanceState != null) {
            hotelList = savedInstanceState.getParcelableArrayList<Hotel>("hotels") as ArrayList<Hotel>
            lytManager.onRestoreInstanceState(savedInstanceState.getParcelable("lytManager"))
            pageOffset = savedInstanceState.getInt("pageOffset")
            isLastPage = savedInstanceState.getBoolean("isLastPage")
        }

    }

    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()

        progressBar = view?.findViewById(R.id.progressBar)!!
        progressBar.visibility = View.GONE

        hotelAdapter = HotelAdapter(hotelList)
        recyclerView = view?.findViewById(R.id.hotelRecyclerView)!!
        recyclerView.apply {
            layoutManager = lytManager
            adapter = hotelAdapter
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
                        pageOffset += 100
                        progressBar.visibility = View.VISIBLE
                        getHotels()
                    }
                }
            }
        )

        if (hotelList.isEmpty()) {
            progressBar.visibility = View.VISIBLE
            getHotels()
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        Log.d(TAG, "onSaveInstanceState")
        outState.putParcelableArrayList("hotels", hotelList)
        outState.putParcelable("lytManager", lytManager.onSaveInstanceState())
        outState.putInt("pageOffset", pageOffset)
        outState.putBoolean("isLastPage", isLastPage)
        super.onSaveInstanceState(outState)
    }

    private fun getHotels() {
        val getHotelsCall: Call<HotelPage> = api.getHotels(pageOffset)
        getHotelsCall.enqueue(object : DefaultCallback<HotelPage?>(requireContext()) {
            @SuppressLint("NotifyDataSetChanged")
            override fun onSuccess(response: Response<HotelPage?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        val responseBody = response.body()!!
                        val hotels = responseBody.results
                        hotelList.addAll(hotels)
                        hotelAdapter.notifyDataSetChanged()

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