package com.voyager.hotels

import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.voyager.databinding.CategoryItemBinding

class CategoryAdapter(var categories: ArrayList<String>
) : RecyclerView.Adapter<CategoryAdapter.ViewHolder>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        return ViewHolder(
            CategoryItemBinding.inflate(
                LayoutInflater.from(parent.context),
                parent,
                false
            )
        )
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.category.text = categories[position]
    }

    override fun getItemCount(): Int = categories.size

    inner class ViewHolder(binding: CategoryItemBinding) : RecyclerView.ViewHolder(binding.root) {
        val category: TextView = binding.category
    }
}