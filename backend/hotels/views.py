import random

from rest_framework import generics
from rest_framework.permissions import AllowAny

from hotels.models import Hotel
from hotels.serializers import HotelSerializer


class HotelView(generics.ListAPIView):
    # preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
    # queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    # TODO change permission
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        # pk_list = list(Hotel.objects.values_list('id', flat=True))
        # pk_list = pk_list[:300]
        # random.shuffle(pk_list)
        # queryset = Hotel.objects.all().filter(pk__in=pk_list)
        # for hotel in queryset:
        #     hotel.recommendation_score = random.randint(1, 100)
        # pk_list = lista id rekomendowanych hoteli dla usera X wraz z ich recommendation_score
        # Przefiltruj queryset po pk_list
        # Nadaj im odpowiednie recommendation_score
        # Posortuj po recommendation_score
        queryset = Hotel.objects.all()
        queryset.filter(city='Nashville')
        return queryset.order_by('stars')
