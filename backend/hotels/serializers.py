import random
from rest_framework import serializers
from hotels.models import Hotel


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
        user_id = self.context['request'].user.id
        print(user_id)

        # tutaj wziąć z jakiejś bazy danych recommendation score dla tego hotelu i tego użytkownika
        if random.randint(0, 1) == 0:
            return 20
        else:
            return 3



    class Meta:
        model = Hotel
        fields = ('name', 'city', 'stars', 'review_count', 'categories', 'recommendation_score')
