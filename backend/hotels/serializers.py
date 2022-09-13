from rest_framework import serializers

from hotels.models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    def get_categories(self, hotel):
        parsed_categories = ""
        categories = hotel.categories[:2]
        for category in categories:
            parsed_categories += f"{category['name']} \n"
        parsed_categories = parsed_categories[:-2]
        return parsed_categories

    class Meta:
        model = Hotel
        fields = ('name', 'city', 'stars', 'review_count', 'categories')
