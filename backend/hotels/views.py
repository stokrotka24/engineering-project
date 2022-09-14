from rest_framework import generics
from rest_framework.permissions import AllowAny

from hotels.models import Hotel
from hotels.serializers import HotelSerializer


class HotelView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    # TODO change permission
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def get_queryset(self):
    #     city = self.request.data['city']
    #     return Hotel.objects.filter(city=city)


