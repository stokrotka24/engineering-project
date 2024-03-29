package com.voyager

import android.os.Bundle
import android.view.MenuItem
import androidx.appcompat.app.ActionBarDrawerToggle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.GravityCompat
import androidx.drawerlayout.widget.DrawerLayout
import com.google.android.material.navigation.NavigationView
import com.voyager.api.ApiUtils
import com.voyager.databinding.ActivityMainBinding
import com.voyager.hotels.SearchFragment
import com.voyager.reviews.UserReviewsFragment
import com.voyager.user.UserFragment

class MainActivity : AppCompatActivity(), NavigationView.OnNavigationItemSelectedListener {
    private lateinit var binding: ActivityMainBinding
    private lateinit var drawer: DrawerLayout

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        val toolbar = binding.toolbar
        setSupportActionBar(toolbar)

        drawer = binding.drawerLayout
        val toggle = ActionBarDrawerToggle(this, drawer, toolbar,
            R.string.navigation_drawer_open, R.string.navigation_drawer_close)
        drawer.addDrawerListener(toggle)
        toggle.syncState()

        val navigationView = binding.navigationView
        navigationView.setNavigationItemSelectedListener(this)
        if (savedInstanceState == null) {
            supportFragmentManager.beginTransaction().replace(R.id.fragmentLayout, SearchFragment()).commit()
            navigationView.setCheckedItem(R.id.nav_hotels)
        }
    }

    override fun onBackPressed() {
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START)
        }
    }

    /**
     * Replaces fragmentLayout with new fragment based on selected item from navigation drawer.
     * If log-out is chosen, finishes MainActivity and returns to the login screen.
     *
     * @param item chosen option from navigation drawer
     */
    override fun onNavigationItemSelected(item: MenuItem): Boolean {
        when(item.itemId) {
            R.id.nav_hotels -> {
                supportFragmentManager.beginTransaction().replace(R.id.fragmentLayout, SearchFragment()).commit()
            }
            R.id.nav_account -> {
                supportFragmentManager.beginTransaction().replace(R.id.fragmentLayout, UserFragment()).commit()
            }
            R.id.nav_reviews -> {
                supportFragmentManager.beginTransaction().replace(R.id.fragmentLayout, UserReviewsFragment()).commit()
            }
            R.id.nav_log_out -> {
                ApiUtils.loggedOut(applicationContext)
                finish()
            }
        }
        drawer.closeDrawer(GravityCompat.START)
        return true
    }
}