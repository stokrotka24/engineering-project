package com.voyager.hotels

import android.content.Context
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.voyager.R
import com.voyager.api.hotels.Attribute
import com.voyager.databinding.AttributeItemBinding


class AttributeAdapter(val context: Context, var attributes: ArrayList<Attribute>
) : RecyclerView.Adapter<AttributeAdapter.ViewHolder>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        return ViewHolder(
            AttributeItemBinding.inflate(
                LayoutInflater.from(parent.context),
                parent,
                false
            )
        )
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val attribute = attributes[position]
        holder.attrName.text = context.getString(R.string.attrName, attribute.name)
        holder.attrValue.text = attribute.value
    }

    override fun getItemCount(): Int = attributes.size

    inner class ViewHolder(binding: AttributeItemBinding) : RecyclerView.ViewHolder(binding.root) {
        val attributeIcon: ImageView = binding.attrIcon
        val attrName: TextView = binding.attrName
        val attrValue: TextView = binding.attrValue
    }
}