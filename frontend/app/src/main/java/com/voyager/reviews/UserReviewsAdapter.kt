package com.voyager.reviews

import android.text.TextUtils
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.RatingBar
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.voyager.api.reviews.UserReview
import com.voyager.databinding.UserReviewItemBinding

private const val MAX_LINES = 4

class UserReviewAdapter(private val reviews: ArrayList<UserReview>, private val listener: OnLongClickListener
) : RecyclerView.Adapter<UserReviewAdapter.ViewHolder>() {
    interface OnLongClickListener {
        fun onItemLongClicked(review: UserReview): Boolean
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        return ViewHolder(
            UserReviewItemBinding.inflate(
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
        holder.hotelName.text = review.hotel_name
        holder.content.text = review.content
        holder.content.maxLines = MAX_LINES
        holder.content.ellipsize = TextUtils.TruncateAt.END

        holder.itemView.setOnClickListener { onItemClicked(holder) }
        holder.itemView.setOnLongClickListener { listener.onItemLongClicked(review) }
    }

    private fun onItemClicked(holder: ViewHolder) {
        val ellipsize = holder.content.ellipsize
        if (ellipsize == null) {
            holder.content.ellipsize = TextUtils.TruncateAt.END
            holder.content.maxLines = MAX_LINES
        } else {
            holder.content.ellipsize = null
            holder.content.maxLines = Int.MAX_VALUE
        }
    }
    override fun getItemCount(): Int = reviews.size

    inner class ViewHolder(binding: UserReviewItemBinding) : RecyclerView.ViewHolder(binding.root) {
        val date: TextView = binding.date
        val ratingBar: RatingBar = binding.stars
        val hotelName: TextView = binding.hotelName
        val content: TextView = binding.content
    }
}