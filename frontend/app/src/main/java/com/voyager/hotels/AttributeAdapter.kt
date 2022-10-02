package com.voyager.hotels

import android.content.Context
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.voyager.R
import com.voyager.api.hotels.Attribute
import com.voyager.databinding.AttributeItemBinding

// TODO move map to some utils
private val attrMap = mapOf(
    "businessAcceptsCreditCards" to Pair("accepts credit cards", R.drawable.ic_baseline_credit_card_24),
    "wiFi" to Pair("Wi-Fi", R.drawable.ic_baseline_wifi_24),
    "restaurantsPriceRange2" to Pair("restaurants price range", R.drawable.ic_baseline_attach_money_24),
    "byAppointmentOnly" to Pair("by appointment only", R.drawable.ic_baseline_navigate_next_24),
    "restaurantsDelivery" to Pair("restaurants delivery", R.drawable.ic_baseline_delivery_dining_24),
    "restaurantsGoodForGroups" to Pair("restaurants good for groups", R.drawable.ic_baseline_groups_24),
    "goodForKids" to Pair("good for kids", R.drawable.ic_baseline_family_restroom_24),
    "outdoorSeating" to Pair("outdoor seating", R.drawable.ic_baseline_navigate_next_24),
    "restaurantsReservations" to Pair("restaurants reservations", R.drawable.ic_baseline_restaurant_24),
    "hasTV" to Pair("has TV", R.drawable.ic_baseline_tv_24),
    "restaurantsTakeOut" to Pair("restaurants take out", R.drawable.ic_baseline_takeout_dining_24),
    "noiseLevel" to Pair("noise level", R.drawable.ic_baseline_surround_sound_24),
    "restaurantsAttire" to Pair("restaurants attire", R.drawable.ic_baseline_style_24),
    "businessAcceptsBitcoin" to Pair("accepts bitcoin", R.drawable.ic_baseline_currency_bitcoin_24),
    "music.dj" to Pair("dj", R.drawable.ic_baseline_music_note_24),
    "music.background_music" to Pair("background music", R.drawable.ic_baseline_music_note_24),
    "music.no_music" to Pair("no music", R.drawable.ic_baseline_music_note_24),
    "music.jukebox" to Pair("jukebox", R.drawable.ic_baseline_music_note_24),
    "music.live" to Pair("live music", R.drawable.ic_baseline_music_note_24), 
    "music.video" to Pair("music video", R.drawable.ic_baseline_music_note_24), 
    "music.karaoke" to Pair("karaoke", R.drawable.ic_baseline_music_note_24),
    "businessParking.garage" to Pair("garage parking", R.drawable.ic_baseline_local_parking_24), 
    "businessParking.street" to Pair("parking on the street", R.drawable.ic_baseline_local_parking_24),
    "businessParking.validated" to Pair("validated parking", R.drawable.ic_baseline_local_parking_24),
    "businessParking.lot" to Pair("parking on the lot", R.drawable.ic_baseline_local_parking_24),
    "businessParking.valet" to Pair("parking valet", R.drawable.ic_baseline_local_parking_24),
    "goodForMeal.breakfast" to Pair("good for breakfast", R.drawable.ic_baseline_restaurant_menu_24),
    "goodForMeal.brunch" to Pair("good for brunch", R.drawable.ic_baseline_restaurant_menu_24),
    "goodForMeal.lunch" to Pair("good for lunch", R.drawable.ic_baseline_restaurant_menu_24),
    "goodForMeal.dinner" to Pair("good for dinner", R.drawable.ic_baseline_restaurant_menu_24),
    "goodForMeal.latenight" to Pair("good for latenight meal", R.drawable.ic_baseline_restaurant_menu_24),
    "goodForMeal.dessert" to Pair("good for dessert", R.drawable.ic_baseline_restaurant_menu_24),
    "BYOBCorkage" to Pair("BYOB corkage", R.drawable.ic_baseline_local_drink_24),
    "smoking" to Pair("smoking", R.drawable.ic_baseline_smoking_rooms_24),
    "BYOB" to Pair("BYOB", R.drawable.ic_baseline_monetization_on_24),
    "restaurantsTableService" to Pair("restaurants table service", R.drawable.ic_baseline_room_service_24),
    "caters" to Pair("caters", R.drawable.ic_baseline_restaurant_menu_24),
    "alcohol" to Pair("alcohol", R.drawable.ic_baseline_local_drink_24),
    "dogsAllowed" to Pair("dogs allowed", R.drawable.ic_baseline_pets_24),
    "wheelchairAccessible" to Pair("wheelchair accessible", R.drawable.ic_baseline_wheelchair_pickup_24),
    "happyHour" to Pair("happy hour", R.drawable.ic_baseline_monetization_on_24),
    "goodForDancing" to Pair("good for dancing", R.drawable.ic_baseline_music_note_24),
    "bestNights.monday" to Pair("best nights on Monday", R.drawable.ic_baseline_nightlife_24),
    "bestNights.tuesday" to Pair("best nights on Tuesday", R.drawable.ic_baseline_nightlife_24),
    "bestNights.wednesday" to Pair("best nights on Wednesday", R.drawable.ic_baseline_nightlife_24),
    "bestNights.thursday" to Pair("best nights on Thursday", R.drawable.ic_baseline_nightlife_24),
    "bestNights.friday" to Pair("best nights on Friday", R.drawable.ic_baseline_nightlife_24),
    "bestNights.saturday" to Pair("best nights on Saturday", R.drawable.ic_baseline_nightlife_24),
    "bestNights.sunday" to Pair("best nights on Sunday", R.drawable.ic_baseline_nightlife_24),
    "ambience.touristy" to Pair("touristy ambience", R.drawable.ic_baseline_style_24),
    "ambience.hipster" to Pair("hipster ambience", R.drawable.ic_baseline_style_24),
    "ambience.romantic" to Pair("romantic ambience", R.drawable.ic_baseline_style_24),
    "ambience.divey" to Pair("divey ambience", R.drawable.ic_baseline_style_24),
    "ambience.intimate" to Pair("intimate ambience", R.drawable.ic_baseline_style_24),
    "ambience.trendy" to Pair("trendy ambience", R.drawable.ic_baseline_style_24),
    "ambience.upscale" to Pair("upscale ambience", R.drawable.ic_baseline_style_24),
    "ambience.classy" to Pair("classy ambience", R.drawable.ic_baseline_style_24),
    "ambience.casual" to Pair("casual ambience", R.drawable.ic_baseline_style_24),
    "coatCheck" to Pair("coat check", R.drawable.ic_baseline_check_circle_outline_24),
    "bikeParking" to Pair("bike parking", R.drawable.ic_baseline_pedal_bike_24),
    "corkage" to Pair("corkage", R.drawable.ic_baseline_local_drink_24),
    "driveThru" to Pair("drive thru", R.drawable.ic_baseline_drive_eta_24),
    "open24Hours" to Pair("open 24 hours", R.drawable.ic_baseline_navigate_next_24),
    "acceptsInsurance" to Pair("accepts insurance", R.drawable.ic_baseline_health_and_safety_24),
    "restaurantsCounterService" to Pair("restaurants counter service", R.drawable.ic_baseline_restaurant_24)
)


class AttributeAdapter(val context: Context, var attributes: ArrayList<Attribute>
) : RecyclerView.Adapter<AttributeAdapter.ViewHolder>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        return ViewHolder(
            AttributeItemBinding.inflate(
                LayoutInflater.from(parent.context),
                parent,
                false
            )
        )
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val attribute = attributes[position]
        val attrInfo = attrMap[attribute.name]!!
        val attrName = attrInfo.first
        val attrIcon = attrInfo.second
        holder.attrIcon.setImageResource(attrIcon)
        holder.attrName.text = context.getString(R.string.attrName, attrName)
        holder.attrValue.text = if (attrName == "restaurants price range") {
            "$".repeat(attribute.value.toInt())
        } else {
            attribute.value
                .replace('_', ' ')
                .replace("False", "no")
                .replace("True", "yes")
        }
    }

    override fun getItemCount(): Int = attributes.size

    inner class ViewHolder(binding: AttributeItemBinding) : RecyclerView.ViewHolder(binding.root) {
        val attrIcon: ImageView = binding.attrIcon
        val attrName: TextView = binding.attrName
        val attrValue: TextView = binding.attrValue
    }
}