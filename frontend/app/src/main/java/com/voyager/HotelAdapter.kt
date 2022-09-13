package com.voyager

import androidx.recyclerview.widget.RecyclerView
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.TextView
import com.voyager.api.hotels.Hotel
import com.voyager.databinding.HotelItemBinding


class HotelAdapter(
    private val hotels: List<Hotel>
) : RecyclerView.Adapter<HotelAdapter.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        return ViewHolder(
            HotelItemBinding.inflate(
                LayoutInflater.from(parent.context),
                parent,
                false
            )
        )
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val hotel = hotels[position]
        holder.name.text = hotel.name
        holder.city.text = hotel.city
        holder.rating.text = hotel.stars.toString()
        holder.reviewCount.text = hotel.review_count.toString()
        holder.categories.text = hotel.categories
    }

    override fun getItemCount(): Int = hotels.size

    inner class ViewHolder(binding: HotelItemBinding) : RecyclerView.ViewHolder(binding.root) {
        val name: TextView = binding.name
        val city: TextView = binding.city
        val rating: TextView = binding.rating
        val reviewCount: TextView = binding.reviewCount
        val categories: TextView = binding.categories
    }

}