package com.voyager.hotels

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.google.android.flexbox.FlexDirection
import com.voyager.R
import com.voyager.api.hotels.HotelDetails
import com.voyager.databinding.ActivityHotelDetailsBinding
import com.google.android.flexbox.FlexboxLayoutManager
import com.google.android.flexbox.JustifyContent
import com.voyager.api.hotels.Attribute


private const val TAG = "HotelDetailsActivity"


class HotelDetailsActivity : AppCompatActivity() {
    private lateinit var binding: ActivityHotelDetailsBinding
    private lateinit var hotel: HotelDetails

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        binding = ActivityHotelDetailsBinding.inflate(layoutInflater)
        setContentView(binding.root)
        hotel = intent.getParcelableArrayListExtra<HotelDetails>("hotel")!![0]

        binding.name.text = hotel.name
        binding.rating.text = hotel.stars
        binding.reviewCount.text = hotel.review_count.toString()
        binding.street.text = hotel.address
        binding.cityState.text = getString(R.string.cityState, hotel.city, hotel.state, hotel.postal_code)
    }

    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()

        val categoryManager = FlexboxLayoutManager(this)
        categoryManager.flexDirection = FlexDirection.ROW
        categoryManager.justifyContent = JustifyContent.FLEX_START
        val categoryAdapter = CategoryAdapter(hotel.categories as ArrayList<String>)
        binding.categoryRecyclerView.apply {
            layoutManager = categoryManager
            adapter = categoryAdapter
        }
        categoryAdapter.notifyDataSetChanged()

        val attributeManager = FlexboxLayoutManager(this)
        attributeManager.flexDirection = FlexDirection.ROW
        attributeManager.justifyContent = JustifyContent.FLEX_START
        val attributeAdapter = AttributeAdapter(applicationContext, hotel.attributes as ArrayList<Attribute>)
        binding.attributesRecyclerView.apply {
            layoutManager = attributeManager
            adapter = attributeAdapter
        }
        attributeAdapter.notifyDataSetChanged()
    }
}