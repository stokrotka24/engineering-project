package com.voyager

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.voyager.databinding.ActivityMainBinding
import okhttp3.OkHttpClient
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory


class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private lateinit var api: ApiInterface

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        val okHttpClient = OkHttpClient().newBuilder().build()
        api = Retrofit.Builder()
            .addConverterFactory(GsonConverterFactory.create())
            .baseUrl(BuildConfig.API_URL)
            .client(okHttpClient)
            .build()
            .create(ApiInterface::class.java)

        binding.getButton.setOnClickListener {
            getHello()
        }
        binding.postButton.setOnClickListener {
            postHello()
        }
    }

    private fun getHello() {
        val getCall = api.postHello()
        getCall.enqueue(object : Callback<ServerHello?> {
            override fun onResponse(call: Call<ServerHello?>, response: Response<ServerHello?>) {
                Log.d("MainActivity", "getHello: onResponse")
                binding.serverTextView.text = response.body()!!.message
            }

            override fun onFailure(call: Call<ServerHello?>, t: Throwable) {
                Log.d("MainActivity", "getHello: onFailure: " + t.message)
            }
        })
    }

    private fun postHello() {
        val name = binding.editTextPersonName.text.toString()
        val clientHello = ClientHello(name)
        val postCall = api.postHello(clientHello)
        postCall.enqueue(object : Callback<ServerHello?> {
            override fun onResponse(call: Call<ServerHello?>, response: Response<ServerHello?>) {
                Log.d("MainActivity", "postHello: onResponse")
                binding.serverTextView.text = response.body()!!.message
            }
            override fun onFailure(call: Call<ServerHello?>, t: Throwable) {
                Log.d("MainActivity", "getHello: onFailure: " + t.message)

            }
        })
    }
}