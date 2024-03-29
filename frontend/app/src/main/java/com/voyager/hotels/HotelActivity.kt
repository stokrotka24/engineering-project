package com.voyager.hotels

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.PopupMenu
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.voyager.R
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.hotels.Hotel
import com.voyager.api.hotels.HotelDetails
import com.voyager.databinding.ActivityHotelBinding
import java.util.*
import kotlin.collections.ArrayList

private const val TAG = "HotelActivity"

class HotelActivity : AppCompatActivity(), FilterFragment.OnMultiChoiceClickListener, HotelAdapter.OnClickListener {
    private lateinit var binding: ActivityHotelBinding
    private lateinit var api: ApiService
    private lateinit var recyclerView: RecyclerView
    private lateinit var hotelAdapter: HotelAdapter
    private lateinit var allHotels: ArrayList<Hotel>
    private lateinit var chosenHotels: ArrayList<Hotel>
    private lateinit var lytManager: LinearLayoutManager
    private lateinit var selectedFilterOptions: BooleanArray
    private var sortType: Int = 0
    private val activityLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()) {
            Log.d(TAG, "Child activity finished: ")
            if (it.resultCode == Activity.RESULT_OK) {
                val hotel = it.data?.getParcelableExtra<HotelDetails>("hotel")
                if (hotel != null) {
                    val hotelInList = allHotels.first { h -> h.id == hotel.id }
                    hotelInList.stars = hotel.stars
                    hotelInList.review_count = hotel.review_count
                }
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        binding = ActivityHotelBinding.inflate(layoutInflater)
        setContentView(binding.root)

        api = ApiUtils.getApi()

        lytManager = LinearLayoutManager(this)
        if (savedInstanceState != null) {
            lytManager.onRestoreInstanceState(savedInstanceState.getParcelable("lytManager"))
            allHotels = savedInstanceState.getParcelableArrayList<Hotel>("allHotels") as ArrayList<Hotel>
            chosenHotels = savedInstanceState.getParcelableArrayList<Hotel>("chosenHotels") as ArrayList<Hotel>
            sortType = savedInstanceState.getInt("sortType")
            selectedFilterOptions = savedInstanceState.getBooleanArray("selectedFilterOptions")!!
        } else {
            allHotels = intent.getParcelableArrayListExtra("hotels")!!
            chosenHotels = ArrayList()
            chosenHotels.addAll(allHotels)
            sortType = R.id.recommDesc
            sortHotels()
            val filterOptions =  resources.getStringArray(R.array.filter_options)
            selectedFilterOptions = BooleanArray(filterOptions.size) { false }
        }

        setToolbar()
        setFiltering()
        setSorting()
    }

    @SuppressLint("NotifyDataSetChanged")
    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()

        hotelAdapter = HotelAdapter(this, chosenHotels)
        recyclerView = binding.hotelRecyclerView
        recyclerView.apply {
            layoutManager = lytManager
            adapter = hotelAdapter
        }
        hotelAdapter.notifyDataSetChanged()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        Log.d(TAG, "onSaveInstanceState")
        outState.putParcelableArrayList("allHotels", allHotels)
        outState.putParcelableArrayList("chosenHotels", chosenHotels)
        outState.putParcelable("lytManager", lytManager.onSaveInstanceState())
        outState.putInt("sortType", sortType)
        outState.putBooleanArray("selectedFilterOptions", selectedFilterOptions)
        super.onSaveInstanceState(outState)
    }

    private fun setToolbar() {
        val toolbar = binding.returnToolbar
        setSupportActionBar(toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setDisplayShowHomeEnabled(true)
        toolbar.setNavigationOnClickListener { onBackPressed() }
    }

    private fun setFiltering() {
        binding.filterBtn.setOnClickListener {
            val filterFragment = FilterFragment(this, selectedFilterOptions.copyOf())
            filterFragment.show(supportFragmentManager, "FilterFragment")
        }
    }

    @SuppressLint("NotifyDataSetChanged")
    private fun setSorting() {
        val sortBtn = binding.sortBtn
        val sortMenu = PopupMenu(this, sortBtn)
        sortMenu.menuInflater.inflate(R.menu.sort_hotels_menu, sortMenu.menu)
        sortMenu.menu.findItem(sortType).isChecked = true
        sortMenu.setOnMenuItemClickListener { item ->
            Log.d(TAG, "setOnMenuItemClickListener: ")
            item.isChecked = true
            sortType = item.itemId
            sortHotels()
            hotelAdapter.notifyDataSetChanged()
            true
        }
        sortBtn.setOnClickListener {
            sortMenu.show()
        }
    }

    private fun sortHotels() {
        when (sortType) {
            R.id.recommDesc -> Collections.sort(chosenHotels, RecommendationComparator(SortOrder.DESC))
            R.id.recommAsc -> Collections.sort(chosenHotels, RecommendationComparator(SortOrder.ASC))
            R.id.ratingDesc -> Collections.sort(chosenHotels, StarsComparator(SortOrder.DESC))
            R.id.ratingAsc -> Collections.sort(chosenHotels, StarsComparator(SortOrder.ASC))
            R.id.reviewsNumDesc -> Collections.sort(chosenHotels, ReviewsNumComparator(SortOrder.DESC))
            R.id.reviewsNumAsc-> Collections.sort(chosenHotels, ReviewsNumComparator(SortOrder.ASC))
        }
    }

    private fun filterHotels(filters: ArrayList<String>) {
        chosenHotels.clear()
        var hotels  = ArrayList<Hotel>()
        hotels.addAll(allHotels)
        for (filter in filters) {
            val filtered: List<Hotel>  = when(filter) {
                getString(R.string.rating_3) -> hotels.filter{ hotel -> hotel.stars >= 3.0 }
                getString(R.string.rating_4) -> hotels.filter{ hotel -> hotel.stars >= 4.0 }
                getString(R.string.reviews_100) -> hotels.filter{ hotel -> hotel.review_count > 100 }
                getString(R.string.reviews_1000) -> hotels.filter{ hotel -> hotel.review_count > 1000 }
                else -> { listOf()}
            }
            hotels = filtered as ArrayList<Hotel>
        }
        chosenHotels.addAll(hotels)
    }

    /**
     * This method is invoked when filter dialog was closed with positive button.
     * Applies selected filter options and filters hotels.
     * After filtering, sorts hotels with chosen sort type.
     *
     * @param selectedFilterOptions filter options selected in filter dialog
     * @see FilterFragment displays filter dialog
     */
    @SuppressLint("NotifyDataSetChanged")
    override fun onClickPositiveButton(selectedFilterOptions: BooleanArray) {
        Log.d(TAG, "onClickPositiveButton: ")
        val filterOptions =  resources.getStringArray(R.array.filter_options)
        this.selectedFilterOptions = selectedFilterOptions
        val filters = ArrayList<String>()
        selectedFilterOptions.forEachIndexed { index, isSelected ->
            if (isSelected) { filters.add(filterOptions[index]) }
        }
        filterHotels(filters)
        sortHotels()
        hotelAdapter.notifyDataSetChanged()
    }

    /**
     * This method is invoked when hotel from list was clicked.
     * Launches activity with details of this hotel.
     *
     * @param hotelId id of clicked hotel
     */
    override fun onItemClicked(hotelId: Int) {
        Log.d(TAG, "onClickRecyclerViewItem: $hotelId")
        val intent = Intent(applicationContext, HotelDetailsActivity::class.java)
        intent.putExtra("hotelId", hotelId)
        activityLauncher.launch(intent)
    }
}