from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from voyager.models import User
from voyager.serializers import RegisterSerializer


class Hello(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        return Response({'message': 'Hello unknown!'})

    def post(self, request, format=None):
        name = request.data['name']
        return Response({'message': f'Hello {name}!'})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
