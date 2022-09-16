from rest_framework import serializers
from hotels.models import Hotel, Recommendation


class HotelSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    recommendation_score = serializers.SerializerMethodField()

    def get_categories(self, hotel):
        parsed_categories = ""
        categories = hotel.categories[:2]
        for category in categories:
            parsed_categories += f"{category['name']} \n"
        parsed_categories = parsed_categories[:-2]
        return parsed_categories

    def get_recommendation_score(self, hotel):
        # user_id = self.context['request'].user.id
        # recommendation = Recommendation.objects.filter(user_id=user_id, hotel_id=hotel.id)
        # score = list(recommendation.values_list('score', flat=True))[0]
        # return score
        user = self.context['request'].user
        score = user.recommendations.index({"hotel_id": hotel.id})
        return score

    class Meta:
        model = Hotel
        fields = ('name', 'city', 'stars', 'review_count', 'categories', 'recommendation_score')
