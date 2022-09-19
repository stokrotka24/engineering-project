package com.voyager.hotels

import android.app.AlertDialog
import android.app.Dialog
import android.content.DialogInterface
import android.os.Bundle
import androidx.fragment.app.DialogFragment
import com.voyager.R

class FilterFragment : DialogFragment() {
    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val builder = AlertDialog.Builder(activity)
        val selectedFilterOptions = ArrayList<String>()
        val filterOptions = resources.getStringArray(R.array.filter_options)
        builder
            .setTitle("Select options")
            .setMultiChoiceItems(filterOptions, null, DialogInterface.OnMultiChoiceClickListener { _, position, isItemChecked ->
                if (isItemChecked) {
                    selectedFilterOptions.add(filterOptions[position])
                } else {
                    selectedFilterOptions.remove(filterOptions[position])
                }
            })
            .setPositiveButton("OK", DialogInterface.OnClickListener { _, _ ->

            })
            .setNegativeButton("Cancel", DialogInterface.OnClickListener { _, _ ->

            })
        return builder.create()
    }
}