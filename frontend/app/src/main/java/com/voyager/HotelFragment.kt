package com.voyager

import android.annotation.SuppressLint
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.LinearLayoutManager
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.api.HttpStatus
import com.voyager.api.hotels.Hotel
import retrofit2.Call
import retrofit2.Response

private const val TAG = "HotelFragment"

class HotelFragment : Fragment() {
    private lateinit var recyclerView: RecyclerView
    private lateinit var hotelAdapter: HotelAdapter
    private var hotelList: ArrayList<Hotel> = ArrayList()
    private lateinit var api: ApiService

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)

        if (savedInstanceState != null) {
            hotelList = savedInstanceState.getParcelableArrayList<Hotel>("hotels") as ArrayList<Hotel>
        }

        api = ApiUtils.getApi()
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        Log.d(TAG, "onCreateView: ")
        return inflater.inflate(R.layout.fragment_hotel, container, false)
    }

    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()

        if (hotelList.isEmpty()) {
            getHotels()
        }

        hotelAdapter = HotelAdapter(hotelList)
        recyclerView = view?.findViewById(R.id.hotelRecyclerView)!!
        recyclerView.apply {
            layoutManager = LinearLayoutManager(view?.context)
            adapter = hotelAdapter
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        Log.d(TAG, "onSaveInstanceState")
        outState.putParcelableArrayList("hotels", hotelList)
        super.onSaveInstanceState(outState)
    }

    private fun getHotels() {
        val getHotelsCall: Call<List<Hotel>> = api.getHotels()
        getHotelsCall.enqueue(object : DefaultCallback<List<Hotel>?>(requireContext()) {
            @SuppressLint("NotifyDataSetChanged")
            override fun onSuccess(response: Response<List<Hotel>?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        val hotels = response.body()!!
                        hotelList.addAll(hotels)
                        hotelAdapter.notifyDataSetChanged()
                    }
                }
            }
        })
    }
}