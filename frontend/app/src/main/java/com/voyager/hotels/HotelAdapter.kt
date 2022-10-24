package com.voyager.hotels

import androidx.recyclerview.widget.RecyclerView
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.TextView
import com.voyager.api.hotels.Hotel
import com.voyager.databinding.HotelItemBinding
import kotlin.collections.ArrayList

private const val TAG = "HotelAdapter"

class HotelAdapter(private val listener: RecyclerViewListener, var chosenHotels: ArrayList<Hotel>
) : RecyclerView.Adapter<HotelAdapter.ViewHolder>() {
    interface RecyclerViewListener {
        fun onItemClicked(id: Int)
    }

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
        val hotel = chosenHotels[position]
        holder.name.text = hotel.name
        holder.city.text = hotel.city
        holder.rating.text = hotel.stars.toString()
        holder.reviewCount.text = hotel.review_count.toString()
        holder.categories.text = hotel.categories.joinToString(",\n")

        holder.itemView.setOnClickListener { listener.onItemClicked(hotel.id) }
    }

    override fun getItemCount(): Int = chosenHotels.size

    inner class ViewHolder(binding: HotelItemBinding) : RecyclerView.ViewHolder(binding.root) {
        val name: TextView = binding.name
        val city: TextView = binding.city
        val rating: TextView = binding.rating
        val reviewCount: TextView = binding.reviewCount
        val categories: TextView = binding.categories
    }
}