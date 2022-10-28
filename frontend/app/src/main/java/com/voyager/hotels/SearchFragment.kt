package com.voyager.hotels


import android.content.Intent
import android.os.Bundle
import android.os.Parcelable
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import com.voyager.R
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.api.HttpStatus
import com.voyager.api.hotels.Hotel
import retrofit2.Call
import retrofit2.Response


private const val TAG = "SearchFragment"
private const val MAX_RECOMMENDATIONS = 100

class SearchFragment : Fragment() {
    private lateinit var cityEditText: EditText
    private lateinit var noRecommendationsEditText: EditText
    private lateinit var recommendationsButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var api: ApiService

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
        api = ApiUtils.getApi()
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        Log.d(TAG, "onCreateView: ")
        return inflater.inflate(R.layout.fragment_search, container, false)
    }

    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()
        bindComponents()
        progressBar.visibility = View.GONE
        setComponentsListeners()

        // TODO remove
        noRecommendationsEditText.setText("9")
    }

    private fun bindComponents() {
        cityEditText = view?.findViewById(R.id.cityEditText)!!
        noRecommendationsEditText = view?.findViewById(R.id.noRecommendationsEditText)!!
        recommendationsButton = view?.findViewById(R.id.requestBtn)!!
        progressBar = view?.findViewById(R.id.progressBar)!!
    }

    private fun setComponentsListeners() {
        cityEditText.setOnClickListener { cityEditText.error = null }
        noRecommendationsEditText.setOnClickListener { noRecommendationsEditText.error = null }
        recommendationsButton.setOnClickListener { recommendationsButtonClicked() }
    }

    private fun recommendationsButtonClicked() {
        val city = cityEditText.text.toString()
        val noRecommendationsText = noRecommendationsEditText.text.toString()
        var noRecommendations = 0
        if (noRecommendationsText.isNotBlank()) {
            try {
                noRecommendations = noRecommendationsText.toInt()
            } catch (ex: NumberFormatException) { } // if noRecommendations is bigger then Int limit
        }

        if (noRecommendations == 0 || noRecommendations> MAX_RECOMMENDATIONS) {
            noRecommendationsEditText.error = "Number of recommendations must be greater than 1 and less than $MAX_RECOMMENDATIONS"
        } else {
            progressBar.visibility = View.VISIBLE
            fetchHotels(city, noRecommendations)
        }
    }

    private fun fetchHotels(city: String, noRecommendations: Int) {
        val getHotelsCall: Call<List<Hotel>> = if (city.isBlank()) {
            api.getHotels(noRecommendations)
        } else {
            api.getHotels(city, noRecommendations)
        }
        getHotelsCall.enqueue(object : DefaultCallback<List<Hotel>?>(activity?.applicationContext!!) {
            override fun onSuccess(response: Response<List<Hotel>?>) {
                progressBar.visibility = View.GONE
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        val hotels = response.body()!!

                        if (hotels.isEmpty()) {
                            cityEditText.error = "We don't have recommendations for this city"
                        } else {
                            val intent = Intent(context, HotelActivity::class.java)
                            intent.putParcelableArrayListExtra("hotels", hotels as ArrayList<out Parcelable>?)
                            startActivity(intent)
                        }
                    }
                }
            }
        })
    }
}