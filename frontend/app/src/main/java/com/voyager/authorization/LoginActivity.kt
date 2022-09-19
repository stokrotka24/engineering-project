package com.voyager.authorization

import android.app.AlertDialog
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
import com.voyager.MainActivity
import com.voyager.R
import com.voyager.api.ApiService
import com.voyager.api.ApiUtils
import com.voyager.api.HttpStatus
import com.voyager.api.login.LoginRequest
import com.voyager.api.registration.RegisterErrors
import com.voyager.api.tokens.TokenManager
import com.voyager.api.tokens.TokenResponse
import com.voyager.databinding.ActivityLoginBinding
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

private const val TAG = "LoginActivity"

class LoginActivity : AppCompatActivity() {
    private lateinit var binding: ActivityLoginBinding
    private lateinit var api: ApiService
    private lateinit var tokenManager: TokenManager
    private lateinit var errorTextView: TextView
    private lateinit var emailField: TextInputLayout
    private lateinit var emailInnerField: TextInputEditText
    private lateinit var passwordField: TextInputLayout
    private lateinit var passwordInnerField: TextInputEditText
    private lateinit var loginButton: Button
    private lateinit var createAccountButton: Button
    private var afterAutoLogOut: Boolean = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        bindComponents()
        setComponentsListeners()
        api = ApiUtils.getApi()
        tokenManager = TokenManager(this)
        afterAutoLogOut = intent.getBooleanExtra("afterAutoLogOut", false)
        Log.d(TAG, "onCreate: afterAutoLogOut = $afterAutoLogOut")
        if (afterAutoLogOut) { displayAutoLogOutDialog() }

        // TODO remove
        emailField.editText?.setText("t@t.com")
        passwordField.editText?.setText("t")
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
        val loginCall: Call<TokenResponse> = api.login(loginRequest)
        loginCall.enqueue(object : Callback<TokenResponse?> {
            override fun onResponse(call: Call<TokenResponse?>, response: Response<TokenResponse?>) {
                val responseCode = response.code()
                Log.d(TAG, "onResponse: response.code = $responseCode")

                when (responseCode) {
                    HttpStatus.OK.code -> {
                        Log.d(TAG, "onResponse: response.body = ${response.body()}")
                        val tokenResponse = response.body()!!
                        tokenManager.saveTokens(tokenResponse.access, tokenResponse.refresh)
                        ApiUtils.loggedIn(applicationContext)
                        Toast.makeText(applicationContext, getString(R.string.logged_in), Toast.LENGTH_LONG).show()
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

            override fun onFailure(call: Call<TokenResponse?>, t: Throwable) {
                Log.d(TAG, "onFailure: ${t.message}")
            }
        })
    }

    private fun displayAutoLogOutDialog() {
        val dialogBuilder = AlertDialog.Builder(this)

        dialogBuilder
            .setTitle("Automatic log out")
            .setMessage(getString(R.string.auto_logged_out))
            .setPositiveButton("OK",null)

        val dialog = dialogBuilder.create()
        dialog.show()
    }

    override fun onBackPressed() {
        if (!afterAutoLogOut) {
            super.onBackPressed()
        }
    }
}