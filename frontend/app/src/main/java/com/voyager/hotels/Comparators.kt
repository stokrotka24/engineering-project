package com.voyager.hotels
import com.voyager.api.hotels.Hotel

enum class SortOrder {
    ASC,
    DESC
}

class RecommendationComparator(private val sortOrder: SortOrder): Comparator<Hotel> {
    /**
     * Provides comparison of hotel recommendation score.
     * The lower the recommendation score, more recommended the hotel is
     *
     * @param hotel1 first hotel to compare
     * @param hotel2 second hotel to compare
     */
    override fun compare(hotel1: Hotel, hotel2: Hotel): Int {
        if (sortOrder == SortOrder.DESC) {
            return hotel1.recommendation_score.compareTo(hotel2.recommendation_score)
        }
        return hotel2.recommendation_score.compareTo(hotel1.recommendation_score)
    }
}

class StarsComparator(private val sortOrder: SortOrder): Comparator<Hotel> {
    override fun compare(hotel1: Hotel, hotel2: Hotel): Int {
        if (sortOrder == SortOrder.DESC) {
            return hotel2.stars.compareTo(hotel1.stars)
        }
        return hotel1.stars.compareTo(hotel2.stars)
    }
}

class ReviewsNumComparator(private val sortOrder: SortOrder): Comparator<Hotel> {
    override fun compare(hotel1: Hotel, hotel2: Hotel): Int {
        if (sortOrder == SortOrder.DESC) {
            return hotel2.review_count.compareTo(hotel1.review_count)
        }
        return hotel1.review_count.compareTo(hotel2.review_count)
    }
}