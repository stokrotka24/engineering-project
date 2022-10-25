from rest_framework import generics, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from hotels.models import Hotel, Review
from hotels.serializers import HotelSerializer, HotelDetailsSerializer, ReviewSerializer, HotelReviewSerializer, \
    UserReviewSerializer, ReviewComplexSerializer


class HotelView(generics.ListAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]

    # TODO delete prints
    def get_queryset(self):
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
        # request.data._mutable = True
        request.data["user_id"] = request.user.id
        # request.data._mutable = False
        return self.create(request, *args, **kwargs)


class HotelReviewsView(generics.ListAPIView):
    serializer_class = HotelReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        hotel_id = self.request.query_params["hotel_id"]
        queryset = Review.objects.filter(hotel_id=hotel_id)
        sort_type = self.request.query_params.get("sort_type")
        if sort_type:
            return queryset.order_by(sort_type)
        return queryset


class UserReviewsView(generics.ListAPIView):
    serializer_class = UserReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Review.objects.filter(user_id=user_id)
        sort_type = self.request.query_params.get("sort_type")
        if sort_type:
            return queryset.order_by(sort_type)
        return queryset


class DeleteReviewView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewComplexSerializer
    permission_classes = [IsAuthenticated]

