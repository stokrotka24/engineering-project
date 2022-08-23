package com.voyager

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.databinding.ActivityMainBinding
import retrofit2.Response

private const val TAG = "MainActivity"

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private lateinit var api: ApiService

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        api = ApiUtils.getApi()

        binding.getButton.setOnClickListener {
            getHello()
        }
        binding.postButton.setOnClickListener {
            postHello()
        }
    }

    private fun getHello() {
        val getCall = api.getHello()
        getCall.enqueue(object : DefaultCallback<ServerHello?>(this) {
            override fun onSuccess(response: Response<ServerHello?>) {
                Log.d(TAG, "onSuccess: getHello")
                binding.serverTextView.text = response.body()!!.message
            }
        })
    }

    private fun postHello() {
        val name = binding.editTextPersonName.text.toString()
        val clientHello = ClientHello(name)
        val postCall = api.postHello(clientHello)
        postCall.enqueue(object : DefaultCallback<ServerHello?>(this) {
            override fun onSuccess(response: Response<ServerHello?>) {
                Log.d(TAG, "onSuccess: postHello")
                binding.serverTextView.text = response.body()!!.message
            }
        })
    }
}