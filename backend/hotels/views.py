from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from hotels.models import Hotel, Review
from hotels.serializers import HotelSerializer, HotelDetailsSerializer, ReviewSerializer


class HotelView(generics.ListAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]

    # TODO delete prints
    def get_queryset(self):
        # user_id = self.request.user.id
        # recommendations_list = Recommendation.objects
        # print(recommendations_list.all())
        # recommendations_list = recommendations_list.filter(user_id=user_id)
        # print(recommendations_list)
        #
        # city = self.request.query_params.get('city')
        # print(city)
        # no_recommendations = int(self.request.query_params.get('no_recommendations'))
        # if city:
        #     hotels_in_city = list(Hotel.objects.filter(city=city).values_list('id', flat=True))
        #     print('if: hotels_in_city', hotels_in_city)
        #     recommendations_list = recommendations_list.filter(hotel_id__in=hotels_in_city)
        #     print('recommendations_list', recommendations_list.values_list('hotel_id', flat=True))
        #
        # recommendations_list = list(recommendations_list.order_by('-score').values_list('hotel_id', flat=True))
        # recommendations_list = recommendations_list[:no_recommendations]
        # print("list", recommendations_list)
        # return Hotel.objects.all().filter(id__in=recommendations_list)
        user = self.request.user
        hotels = Hotel.objects
        recommendations = user.recommendations
        print(recommendations[0])
        city = self.request.query_params.get('city')
        print(city)
        no_recommendations = int(self.request.query_params.get('no_recommendations'))
        if city:
            recommendations_for_city = []
            hotels = Hotel.objects.filter(city=city)
            hotels_ids_in_city = list(hotels.values_list('id', flat=True))
            print('if: hotels_in_city', hotels_ids_in_city)
            for r in recommendations:
                if r["hotel_id"] in hotels_ids_in_city:
                    recommendations_for_city.append(r)
            recommendations = recommendations_for_city

        recommendations = recommendations[:no_recommendations]
        hotel_ids = [r["hotel_id"] for r in recommendations]
        return hotels.filter(id__in=hotel_ids)


class HotelDetailsView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailsSerializer
    permission_classes = [IsAuthenticated]


class CreateReviewView(mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data["user_id"] = request.user.id
        request.data._mutable = False
        return self.create(request, *args, **kwargs)
