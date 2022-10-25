from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authorization.models import User
from authorization.serializers import RegisterSerializer, ChangePasswordSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]


class AccountInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        return Response({'id': user_id, 'username': user.username, 'email': user.email})
