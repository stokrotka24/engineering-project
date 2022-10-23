package com.voyager.hotels

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.RatingBar
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.voyager.api.hotels.ReviewDetails
import com.voyager.databinding.ReviewItemBinding

class ReviewAdapter(private val reviews: ArrayList<ReviewDetails>
) : RecyclerView.Adapter<ReviewAdapter.ViewHolder>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        return ViewHolder(
            ReviewItemBinding.inflate(
                LayoutInflater.from(parent.context),
                parent,
                false
            )
        )
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val review = reviews[position]
        holder.date.text = review.date
        holder.ratingBar.rating = review.stars.toFloat()
        holder.userName.text = review.username
        holder.content.text = review.content
    }

    override fun getItemCount(): Int = reviews.size

    inner class ViewHolder(binding: ReviewItemBinding) : RecyclerView.ViewHolder(binding.root) {
        val date: TextView = binding.date
        val ratingBar: RatingBar = binding.stars
        val userName: TextView = binding.username
        val content: TextView = binding.content }
}