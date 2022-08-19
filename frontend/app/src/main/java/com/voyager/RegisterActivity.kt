package com.voyager

import android.os.Bundle
import android.util.Log
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.textfield.TextInputLayout
import com.google.gson.Gson
import com.voyager.api.ApiInterface
import com.voyager.api.ApiService
import com.voyager.databinding.ActivityRegisterBinding
import org.json.JSONObject
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


private const val TAG = "RegisterActivity"

class RegisterActivity : AppCompatActivity() {
    private lateinit var binding: ActivityRegisterBinding
    private lateinit var api: ApiInterface
    private lateinit var usernameField: TextInputLayout
    private lateinit var emailField: TextInputLayout
    private lateinit var passwordField: TextInputLayout
    private lateinit var passwordConfirmField: TextInputLayout
    private lateinit var registerButton: Button


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRegisterBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        bindComponents()
        api = ApiService.getApi()
    }

    private fun bindComponents() {
        binding.let {
            usernameField = it.usernameTextField
            emailField = it.emailTextField
            passwordField = it.passwordTextField
            passwordConfirmField = it.passwordConfirmTextField
            registerButton = it.registerButton
        }

        registerButton.setOnClickListener {
            Log.d(TAG, "bindComponents: registerButton.onClick: ")
            val username = usernameField.editText?.text.toString()
            val email = emailField.editText?.text.toString()
            val password = passwordField.editText?.text.toString()
            val passwordConfirmation = passwordConfirmField.editText?.text.toString()
            tryRegister(username, email, password, passwordConfirmation)
        }
    }

    private fun tryRegister(username: String, email: String, password: String, passwordConfirm: String) {
        val registerRequest = RegisterRequest(username, email, password, passwordConfirm)
        val registerCall:Call<JSONObject> = api.register(registerRequest)
        registerCall.enqueue(object : Callback<JSONObject?> {
            override fun onResponse(call: Call<JSONObject?>, response: Response<JSONObject?>) {
                if (response.code() == 400) {
                    val errorBody = response.errorBody()?.string()
                    Log.d(TAG, "onResponse: response.code = 400, error = $errorBody")

                    val registerErrors = Gson().fromJson(errorBody, RegisterErrors::class.java)
                    usernameField.error = registerErrors.username?.get(0)
                    val emailError = registerErrors.email
                    if (emailError != null) {
                        if (emailError.get(0) == getString(R.string.non_unique_field)) {
                            emailField.error = getString(R.string.user_with_this_email_already_exists)
                        } else {
                            emailField.error = registerErrors.email.get(0)
                        }
                    }
                    passwordField.error = registerErrors.password?.get(0)
                    passwordConfirmField.error = registerErrors.password_confirmation?.get(0)
                } else {
                    Log.d(TAG, "onResponse: response =${response.body().toString()}")
                }

            }

            override fun onFailure(call: Call<JSONObject?>, t: Throwable) {
                Log.d(TAG, "onFailure: ")
            }
        })
       
    }
}