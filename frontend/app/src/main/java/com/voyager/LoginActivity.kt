package com.voyager

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import com.google.gson.Gson
import com.voyager.api.ApiInterface
import com.voyager.api.ApiService
import com.voyager.databinding.ActivityLoginBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

private const val TAG = "LoginActivity"

class LoginActivity : AppCompatActivity() {
    private lateinit var binding: ActivityLoginBinding
    private lateinit var api: ApiInterface
    private lateinit var errorTextView: TextView
    private lateinit var emailField: TextInputLayout
    private lateinit var emailInnerField: TextInputEditText
    private lateinit var passwordField: TextInputLayout
    private lateinit var passwordInnerField: TextInputEditText
    private lateinit var loginButton: Button
    private lateinit var createAccountButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        bindComponents()
        setComponentsListeners()
        api = ApiService.getApi()
    }

    private fun bindComponents() {
        binding.let {
            errorTextView = it.loginErrorTextView

            emailField = it.emailTextField
            emailInnerField = it.emailInnerTextField

            passwordField = it.passwordTextField
            passwordInnerField = it.passwordInnerTextField

            loginButton = it.loginButton
            createAccountButton = it.createAccountButton
        }
    }

    private fun setComponentsListeners() {
        emailField.setOnClickListener { emailField.error = null }
        emailInnerField.setOnClickListener { emailField.error = null }

        passwordInnerField.setOnClickListener { passwordField.error = null }
        passwordField.setOnClickListener { passwordField.error = null }

        loginButton.setOnClickListener { loginButtonClicked() }
        createAccountButton.setOnClickListener { createAccountButtonClicked() }
    }

    private fun loginButtonClicked() {
        errorTextView.text = null
        emailField.error = null
        passwordField.error = null

        val email = emailField.editText?.text.toString()
        val password = passwordField.editText?.text.toString()
        tryLogin(email, password)
    }

    private fun createAccountButtonClicked() {
        val intent = Intent(this, RegisterActivity::class.java)
        startActivity(intent)
    }

    private fun tryLogin(email: String, password: String) {
        val loginRequest = LoginRequest(email, password)
        val loginCall: Call<LoginResponse> = api.login(loginRequest)
        loginCall.enqueue(object : Callback<LoginResponse?> {
            override fun onResponse(call: Call<LoginResponse?>, response: Response<LoginResponse?>) {
                val responseCode = response.code()
                Log.d(TAG, "onResponse: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        Log.d(TAG, "onResponse: response.body = ${response.body()}")
                        Toast.makeText(applicationContext, getString(R.string.logged_in), Toast.LENGTH_LONG).show()
                        Thread.sleep(1_000)
                        val intent = Intent(applicationContext, MainActivity::class.java)
                        startActivity(intent)
                    }

                    HttpStatus.BadRequest.code -> {
                        val errorBody = response.errorBody()?.string()
                        Log.d(TAG, "onResponse: error.body = $errorBody")

                        val registerErrors = Gson().fromJson(errorBody, RegisterErrors::class.java)
                        emailField.error = registerErrors.email?.get(0)
                        passwordField.error = registerErrors.password?.get(0)
                    }

                    HttpStatus.Unauthorized.code -> {
                        val errorBody = response.errorBody()?.string()
                        Log.d(TAG, "onResponse: error.body = $errorBody")

                        errorTextView.text = getString(R.string.login_error)
                        emailField.error = " "
                        passwordField.error = " "
                    }

                    else -> {
                        Toast.makeText(applicationContext, getString(R.string.server_error), Toast.LENGTH_LONG).show()
                    }
                }
            }

            override fun onFailure(call: Call<LoginResponse?>, t: Throwable) {
                Log.d(TAG, "onFailure: ${t.message}")
            }
        })
    }
}