package com.voyager.authorization

import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.google.gson.Gson
import com.voyager.R
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.HttpStatus
import com.voyager.api.registration.RegisterErrors
import com.voyager.api.registration.RegisterRequest
import com.voyager.api.registration.RegisterResponse
import com.voyager.databinding.ActivityRegisterBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


private const val TAG = "RegisterActivity"

class RegisterActivity : AppCompatActivity() {
    private lateinit var binding: ActivityRegisterBinding
    private lateinit var api: ApiService
    private lateinit var usernameField: TextInputLayout
    private lateinit var usernameInnerField: TextInputEditText
    private lateinit var emailField: TextInputLayout
    private lateinit var emailInnerField: TextInputEditText
    private lateinit var passwordField: TextInputLayout
    private lateinit var passwordInnerField: TextInputEditText
    private lateinit var passwordConfirmField: TextInputLayout
    private lateinit var passwordConfirmInnerField: TextInputEditText
    private lateinit var registerButton: Button


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRegisterBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        bindComponents()
        setComponentsListeners()
        api = ApiUtils.getApi()
    }

    private fun bindComponents() {
        binding.let {
            usernameField = it.usernameTextField
            usernameInnerField = it.usernameInnerTextField

            emailField = it.emailTextField
            emailInnerField = it.emailInnerTextField

            passwordField = it.passwordTextField
            passwordInnerField = it.passwordInnerTextField

            passwordConfirmField = it.passwordConfirmTextField
            passwordConfirmInnerField = it.passwordConfirmInnerTextField

            registerButton = it.registerButton
        }
    }
    
    private fun setComponentsListeners() {
        usernameField.setOnClickListener { usernameField.error = null }
        usernameInnerField.setOnClickListener { usernameField.error = null }
        
        emailField.setOnClickListener { emailField.error = null }
        emailInnerField.setOnClickListener { emailField.error = null }

        passwordInnerField.setOnClickListener { passwordField.error = null }
        passwordField.setOnClickListener { passwordField.error = null }

        passwordConfirmInnerField.setOnClickListener { passwordConfirmField.error = null }
        passwordConfirmField.setOnClickListener { passwordConfirmField.error = null }
        
        registerButton.setOnClickListener { registerButtonClicked() }
    }

    private fun registerButtonClicked() {
        usernameField.error = null
        emailField.error = null
        passwordField.error = null
        passwordConfirmField.error = null

        val username = usernameField.editText?.text.toString()
        val email = emailField.editText?.text.toString()
        val password = passwordField.editText?.text.toString()
        val passwordConfirmation = passwordConfirmField.editText?.text.toString()
        tryRegister(username, email, password, passwordConfirmation)
    }

    private fun tryRegister(username: String, email: String, password: String, passwordConfirm: String) {
        val registerRequest = RegisterRequest(username, email, password, passwordConfirm)
        val registerCall:Call<RegisterResponse> = api.register(registerRequest)
        registerCall.enqueue(object : Callback<RegisterResponse?> {
            override fun onResponse(call: Call<RegisterResponse?>, response: Response<RegisterResponse?>) {
                val responseCode = response.code()
                Log.d(TAG, "onResponse: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.Created.code -> {
                        Log.d(TAG, "onResponse: response.body = ${response.body()}")
                        Toast.makeText(applicationContext, getString(R.string.account_created), Toast.LENGTH_LONG).show()
                        Thread.sleep(1_000)
                        finish()
                    }

                    HttpStatus.BadRequest.code -> {
                        val errorBody = response.errorBody()?.string()
                        Log.d(TAG, "onResponse: error.body = $errorBody")

                        val registerErrors = Gson().fromJson(errorBody, RegisterErrors::class.java)
                        usernameField.error = registerErrors.username?.get(0)
                        val emailError = registerErrors.email
                        if (emailError != null) {
                            if (emailError.get(0) == getString(R.string.non_unique_field)) {
                                emailField.error = getString(R.string.user_with_this_email_already_exists)
                            } else {
                                emailField.error = emailError.get(0)
                            }
                        }
                        passwordField.error = registerErrors.password?.get(0)
                        passwordConfirmField.error = registerErrors.password_confirmation?.get(0)
                    }

                    else -> {
                        Toast.makeText(applicationContext, getString(R.string.server_error), Toast.LENGTH_LONG).show()
                    }
                }
            }

            override fun onFailure(call: Call<RegisterResponse?>, t: Throwable) {
                Log.d(TAG, "onFailure: ${t.message}")
            }
        })
       
    }
}