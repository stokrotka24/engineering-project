package com.voyager.user

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.Toast
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.google.gson.Gson
import com.voyager.R
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.DefaultCallback
import com.voyager.api.HttpStatus
import com.voyager.api.user.*
import com.voyager.databinding.ActivityChangePasswordBinding
import retrofit2.Call
import retrofit2.Response

private const val TAG = "ChangePasswordActivity"

class ChangePasswordActivity : AppCompatActivity() {
    private lateinit var binding: ActivityChangePasswordBinding
    private lateinit var api: ApiService
    private var userId:Int = -1
    private lateinit var oldPasswordField: TextInputLayout
    private lateinit var oldPasswordInnerField: TextInputEditText
    private lateinit var passwordField: TextInputLayout
    private lateinit var passwordInnerField: TextInputEditText
    private lateinit var passwordConfirmField: TextInputLayout
    private lateinit var passwordConfirmInnerField: TextInputEditText
    private lateinit var changePasswordButton: Button


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityChangePasswordBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)
        userId = intent.getIntExtra("userId", -1)

        bindComponents()
        setComponentsListeners()
        api = ApiUtils.getApi()
    }

    private fun bindComponents() {
        binding.let {
            oldPasswordField = it.oldPasswordTextField
            oldPasswordInnerField = it.oldPasswordInnerTextField
            
            passwordField = it.passwordTextField
            passwordInnerField = it.passwordInnerTextField

            passwordConfirmField = it.passwordConfirmTextField
            passwordConfirmInnerField = it.passwordConfirmInnerTextField

            changePasswordButton = it.registerButton
        }
    }

    private fun setComponentsListeners() {
        oldPasswordInnerField.setOnClickListener { oldPasswordField.error = null }
        oldPasswordField.setOnClickListener { oldPasswordField.error = null }

        passwordInnerField.setOnClickListener { passwordField.error = null }
        passwordField.setOnClickListener { passwordField.error = null }

        passwordConfirmInnerField.setOnClickListener { passwordConfirmField.error = null }
        passwordConfirmField.setOnClickListener { passwordConfirmField.error = null }

        changePasswordButton.setOnClickListener { changePasswordButtonClicked() }
    }

    private fun changePasswordButtonClicked() {
        oldPasswordField.error = null
        passwordField.error = null
        passwordConfirmField.error = null

        val oldPassword = oldPasswordField.editText?.text.toString()
        val password = passwordField.editText?.text.toString()
        val passwordConfirmation = passwordConfirmField.editText?.text.toString()
        tryChangePassword(oldPassword, password, passwordConfirmation)
    }

    private fun tryChangePassword(oldPassword: String, password: String, passwordConfirm: String) {
        val changePassRequest = ChangePassRequest(oldPassword, password, passwordConfirm)
        val changePassCall: Call<ChangePassResponse> = api.changePassword(userId, changePassRequest)
        changePassCall.enqueue(object : DefaultCallback<ChangePassResponse?>(this) {
            override fun onSuccess(response: Response<ChangePassResponse?>) {
                val responseCode = response.code()
                Log.d(TAG, "onSuccess: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        Log.d(TAG, "onResponse: response.body = ${response.body()}")
                        Toast.makeText(applicationContext, "Password successfully changed", Toast.LENGTH_LONG).show()
                        val intent = Intent(applicationContext, LoginActivity::class.java)
                        startActivity(intent)
                    }

                    HttpStatus.BadRequest.code -> {
                        val errorBody = response.errorBody()?.string()
                        Log.d(TAG, "onResponse: error.body = $errorBody")

                        val changePassErrors = Gson().fromJson(errorBody, ChangePassErrors::class.java)
                        oldPasswordField.error = changePassErrors.old_password?.get(0)
                        passwordField.error = changePassErrors.password?.get(0)
                        passwordConfirmField.error = changePassErrors.password_confirmation?.get(0)
                    }

                    else -> {
                        Toast.makeText(applicationContext, getString(R.string.server_error), Toast.LENGTH_LONG).show()
                    }
                }
            }
        })

    }
}