from rest_framework import serializers
from hotels.models import Hotel, Recommendation, Review


class HotelSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    recommendation_score = serializers.SerializerMethodField()

    def get_categories(self, hotel):
        return [category["name"] for category in hotel.categories[:3]]

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
        fields = ('id', 'name', 'city', 'stars', 'review_count', 'categories', 'recommendation_score')


class HotelDetailsSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_categories(self, hotel):
        return [category["name"] for category in hotel.categories]

    def get_attributes(self, hotel):
        attributes = {}
        enum_fields = {"wiFi", "noiseLevel", "restaurantsAttire", "BYOBCorkage", "smoking", "alcohol"}
        embedded_fields = {"music", "businessParking", "goodForMeal", "bestNights", "ambience"}

        for (attr_key, attr_val) in hotel.attributes.items():
            if attr_key in embedded_fields:
                for (emb_attr_key, emb_attr_val) in hotel.attributes[attr_key].items():
                    if emb_attr_val is True:
                        attributes[attr_key + "." + emb_attr_key] = str(emb_attr_val)
            else:
                if attr_val is not None:
                    if attr_key in enum_fields:
                        attributes[attr_key] = attr_val.name
                    else:
                        attributes[attr_key] = str(attr_val)

        attributes_as_list = []
        for (attr_key, attr_val) in attributes.items():
            attributes_as_list.append({"name": attr_key, "value": attr_val})

        return attributes_as_list

    class Meta:
        model = Hotel
        fields = ('id', 'name', 'address', 'city', 'state', 'postal_code',
                  'stars', 'review_count', 'categories', 'attributes')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('user_id', 'hotel_id', 'stars', 'content')
