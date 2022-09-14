package com.voyager

import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils


private const val TAG = "HotelFragment"

class HotelFragment : Fragment() {
    private lateinit var getRecommendationsButton: Button
    private lateinit var api: ApiService

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        api = ApiUtils.getApi()
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        Log.d(TAG, "onCreateView: ")
        return inflater.inflate(R.layout.fragment_hotel, container, false)
    }

    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()
//        getRecommendationsButton = view?.findViewById(R.id.button)!!
//        getRecommendationsButton.setOnClickListener {
//            val intent = Intent(context, HotelActivity::class.java)
//            startActivity(intent)
//        }
    }
}