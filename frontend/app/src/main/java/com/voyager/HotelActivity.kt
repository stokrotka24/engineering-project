package com.voyager

import android.annotation.SuppressLint
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.api.HttpStatus
import com.voyager.api.hotels.Hotel
import com.voyager.api.hotels.HotelPage
import com.voyager.databinding.ActivityHotelBinding
import retrofit2.Call
import retrofit2.Response

private const val TAG = "HotelActivity"

class HotelActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHotelBinding
    private lateinit var api: ApiService
    private lateinit var recyclerView: RecyclerView
    private lateinit var hotelAdapter: HotelAdapter
    private var hotelList: ArrayList<Hotel> = ArrayList()
    private lateinit var lytManager: LinearLayoutManager

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        binding = ActivityHotelBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        api = ApiUtils.getApi()

        lytManager = LinearLayoutManager(this)
        if (savedInstanceState != null) {
            hotelList = savedInstanceState.getParcelableArrayList<Hotel>("hotels") as ArrayList<Hotel>
            lytManager.onRestoreInstanceState(savedInstanceState.getParcelable("lytManager"))
        }
    }

    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()

        hotelAdapter = HotelAdapter(hotelList)
        recyclerView = binding.hotelRecyclerView
        recyclerView.apply {
            layoutManager = lytManager
            adapter = hotelAdapter
        }

        if (hotelList.isEmpty()) {
            Log.d(TAG, "onStart: hotelList is empty")
            getHotels()
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        Log.d(TAG, "onSaveInstanceState")
        outState.putParcelableArrayList("hotels", hotelList)
        outState.putParcelable("lytManager", lytManager.onSaveInstanceState())
        super.onSaveInstanceState(outState)
    }

    private fun getHotels() {
        val getHotelsCall: Call<HotelPage> = api.getHotels()
        getHotelsCall.enqueue(object : DefaultCallback<HotelPage?>(this) {
            @SuppressLint("NotifyDataSetChanged")
            override fun onSuccess(response: Response<HotelPage?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        val hotels = response.body()!!.results
                        hotelList.addAll(hotels)
                        hotelAdapter.notifyDataSetChanged()
                    }
                }
            }
        })
    }

}