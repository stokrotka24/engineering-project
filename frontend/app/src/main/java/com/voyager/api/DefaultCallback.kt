package com.voyager.api

import android.content.Context
import android.content.Intent
import android.util.Log
import com.voyager.LoginActivity

import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

private const val TAG = "DefaultCallback"

abstract class DefaultCallback<T>(private val context: Context): Callback<T> {
    override fun onResponse(call: Call<T>, response: Response<T>) {
        if (response.code() == HttpStatus.Unauthorized.code) {
            val intent = Intent(context, LoginActivity::class.java)
            intent.putExtra("afterAutoLogOut", true)
            context.startActivity(intent)
        } else {
            onSuccess(response)
        }
    }

    abstract fun onSuccess(response: Response<T>)

    override fun onFailure(call: Call<T>, t: Throwable) {
        Log.d(TAG, "onFailure: ${t.message}")
    }

}