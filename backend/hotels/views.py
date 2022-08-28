from rest_framework import generics
from rest_framework.permissions import AllowAny

from hotels.models import Hotel
from hotels.serializers import HotelSerializer


class HotelView(generics.CreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    # TODO change permission
    permission_classes = [AllowAny]

