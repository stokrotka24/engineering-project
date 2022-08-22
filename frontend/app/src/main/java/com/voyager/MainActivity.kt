package com.voyager

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.BaseCallback
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
//        getCall.enqueue(object : Callback<ServerHello?> {
//            override fun onResponse(call: Call<ServerHello?>, response: Response<ServerHello?>) {
//                Log.d(TAG, "getHello: onResponse")
//
//                if (response.code() == HttpStatus.Unauthorized.code) {
//                    startActivity(Intent(applicationContext, LoginActivity::class.java))
//                } else {
//                    binding.serverTextView.text = response.body()!!.message
//                }
//            }
//
//            override fun onFailure(call: Call<ServerHello?>, t: Throwable) {
//                Log.d(TAG, "getHello: onFailure: " + t.message)
//            }
//        })
        getCall.enqueue(object : BaseCallback<ServerHello?>(this) {
            override fun onSuccess(response: Response<ServerHello?>) {
                binding.serverTextView.text = response.body()!!.message
            }
        })
    }

    private fun postHello() {
        val name = binding.editTextPersonName.text.toString()
        val clientHello = ClientHello(name)
        val postCall = api.postHello(clientHello)
//        postCall.enqueue(object : Callback<ServerHello?> {
//            override fun onResponse(call: Call<ServerHello?>, response: Response<ServerHello?>) {
//                Log.d(TAG, "postHello: onResponse")
//                if (response.code() == HttpStatus.Unauthorized.code) {
//                    startActivity(Intent(applicationContext, LoginActivity::class.java))
//                } else{
//                    binding.serverTextView.text = response.body()!!.message
//                }
//            }
//            override fun onFailure(call: Call<ServerHello?>, t: Throwable) {
//                Log.d(TAG, "getHello: onFailure: " + t.message)
//
//            }
//        })
        postCall.enqueue(object : BaseCallback<ServerHello?>(this) {
            override fun onSuccess(response: Response<ServerHello?>) {
                binding.serverTextView.text = response.body()!!.message
            }
        })
    }
}