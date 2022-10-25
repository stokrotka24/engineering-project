package com.voyager.user

import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import com.voyager.R
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.api.HttpStatus
import com.voyager.api.user.UserAccount
import retrofit2.Call
import retrofit2.Response
import kotlin.math.log

private const val TAG = "UserFragment"

class UserFragment : Fragment() {
    private lateinit var usernameTextView: TextView
    private lateinit var emailTextView: TextView
    private var userId: Int? = null
    private lateinit var progressBar: ProgressBar
    private lateinit var editPassButton: Button
    
    override fun onCreate(savedInstanceState: Bundle?) {
        Log.d(TAG, "onCreate: ")
        super.onCreate(savedInstanceState)
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        Log.d(TAG, "onCreateView: ")
        return inflater.inflate(R.layout.fragment_user, container, false)
    }

    override fun onStart() {
        Log.d(TAG, "onStart: ")
        super.onStart()

        usernameTextView = view?.findViewById(R.id.usernameTextView)!!
        emailTextView = view?.findViewById(R.id.emailTextView)!!
        progressBar = view?.findViewById(R.id.progressBar)!!
        editPassButton = view?.findViewById(R.id.editPasswordButton)!!

        progressBar.visibility = View.VISIBLE
        val api = ApiUtils.getApi()
        val getAccountInfoCall: Call<UserAccount> = api.getAccountInfo()
        getAccountInfoCall.enqueue(object : DefaultCallback<UserAccount?>(requireContext()) {
            override fun onSuccess(response: Response<UserAccount?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        val userAccount = response.body()!!
                        usernameTextView.text = userAccount.username
                        emailTextView.text = userAccount.email
                        userId = userAccount.id
                        progressBar.visibility = View.GONE
                        editPassButton.setOnClickListener { editPassButtonClicked() }
                    }
                }
            }
        })
    }

    private fun editPassButtonClicked() {
        Log.d(TAG, "editPassButtonClicked: ")
        val intent = Intent(context, ChangePasswordActivity::class.java)
        intent.putExtra("userId", userId)
        startActivity(intent)
    }
}