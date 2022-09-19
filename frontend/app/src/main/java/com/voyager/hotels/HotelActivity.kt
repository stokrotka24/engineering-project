package com.voyager.hotels

import android.annotation.SuppressLint
import android.os.Bundle
import android.util.Log
import android.widget.PopupMenu
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.voyager.R
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.hotels.Hotel
import com.voyager.databinding.ActivityHotelBinding

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

        val toolbar = binding.returnToolbar
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setDisplayShowHomeEnabled(true)
        toolbar.setNavigationOnClickListener { onBackPressed() }

        val filterBtn = binding.filterBtn
        filterBtn.setOnClickListener {
            val filterFragment = FilterFragment()
            filterFragment.show(supportFragmentManager, "FilterFragment")
        }

        val sortBtn = binding.sortBtn
        val sortMenu = PopupMenu(this, sortBtn)
        sortMenu.menuInflater.inflate(R.menu.sort_menu, sortMenu.menu)
        sortMenu.setOnMenuItemClickListener { item ->
            Log.d(TAG, "onMenuItemClick: ")
            item.isChecked = !item.isChecked
            when (item.itemId) {
                R.id.recommendationDec -> "d"
            }

            true
        }
        sortBtn.setOnClickListener {
            sortMenu.show()
        }


        lytManager = LinearLayoutManager(this)
        if (savedInstanceState != null) {
            hotelList = savedInstanceState.getParcelableArrayList<Hotel>("hotels") as ArrayList<Hotel>
            lytManager.onRestoreInstanceState(savedInstanceState.getParcelable("lytManager"))
        } else {
            hotelList = intent.getParcelableArrayListExtra("hotels")!!
        }
    }

    @SuppressLint("NotifyDataSetChanged")
    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()

        hotelAdapter = HotelAdapter(hotelList)
        recyclerView = binding.hotelRecyclerView
        recyclerView.apply {
            layoutManager = lytManager
            adapter = hotelAdapter
        }
        hotelAdapter.notifyDataSetChanged()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        Log.d(TAG, "onSaveInstanceState")
        outState.putParcelableArrayList("hotels", hotelList)
        outState.putParcelable("lytManager", lytManager.onSaveInstanceState())
        super.onSaveInstanceState(outState)
    }
}