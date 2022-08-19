package com.voyager

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.voyager.api.ApiInterface
import com.voyager.api.ApiService
import com.voyager.databinding.ActivityMainBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

private const val TAG = "MainActivity"

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private lateinit var api: ApiInterface

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        api = ApiService.getApi()

        binding.getButton.setOnClickListener {
            getHello()
        }
        binding.postButton.setOnClickListener {
            postHello()
        }
    }

    private fun getHello() {
        val getCall = api.getHello()
        getCall.enqueue(object : Callback<ServerHello?> {
            override fun onResponse(call: Call<ServerHello?>, response: Response<ServerHello?>) {
                Log.d(TAG, "getHello: onResponse")
                binding.serverTextView.text = response.body()!!.message
            }

            override fun onFailure(call: Call<ServerHello?>, t: Throwable) {
                Log.d(TAG, "getHello: onFailure: " + t.message)
            }
        })
    }

    private fun postHello() {
        val name = binding.editTextPersonName.text.toString()
        val clientHello = ClientHello(name)
        val postCall = api.postHello(clientHello)
        postCall.enqueue(object : Callback<ServerHello?> {
            override fun onResponse(call: Call<ServerHello?>, response: Response<ServerHello?>) {
                Log.d(TAG, "postHello: onResponse")
                binding.serverTextView.text = response.body()!!.message
            }
            override fun onFailure(call: Call<ServerHello?>, t: Throwable) {
                Log.d(TAG, "getHello: onFailure: " + t.message)

            }
        })
    }
}