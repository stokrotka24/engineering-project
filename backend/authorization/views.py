from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authorization.models import User
from authorization.serializers import RegisterSerializer, ChangePasswordSerializer


class RegisterView(generics.CreateAPIView):
    """
    Creates a new user instance.
    If registration succeeded, returns username and email of created user.
    Otherwise, returns registration problems e.g. difference between password
    and password confirmation.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ChangePasswordView(generics.UpdateAPIView):
    """
    Changes user password.
    If changing password succeeded, returns user id, username and email.
    Otherwise, returns changing password problems e.g. difference between password
    and password confirmation.
    """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]


class AccountInfoView(APIView):
    """
    Returns user data: id, username, email.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        return Response({'id': user_id, 'username': user.username, 'email': user.email})
