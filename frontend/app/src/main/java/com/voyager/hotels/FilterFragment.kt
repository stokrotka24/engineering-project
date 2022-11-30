package com.voyager.hotels

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import androidx.fragment.app.DialogFragment
import com.voyager.R

/**
 * Displays dialog with filter options.
 *
 * @param listener listener, who will be notified about new selected filter options
 *                 when positive button will be clicked
 * @param selectedFilterOptions currently selected filter options to display in dialog
 */
class FilterFragment(private val listener: OnMultiChoiceClickListener, private val selectedFilterOptions: BooleanArray) : DialogFragment() {
    interface OnMultiChoiceClickListener {
        fun onClickPositiveButton(selectedFilterOptions: BooleanArray)
    }

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val filterOptions = resources.getStringArray(R.array.filter_options)

        val builder = AlertDialog.Builder(activity)
        builder.setTitle("Select filters")
            .setMultiChoiceItems(filterOptions, selectedFilterOptions) { _, position, isItemChecked ->
                selectedFilterOptions[position] = isItemChecked
            }.setPositiveButton("OK") { _, _ ->
                listener.onClickPositiveButton(selectedFilterOptions)
            }.setNegativeButton("Cancel") { _, _ -> }
        return builder.create()
    }
}