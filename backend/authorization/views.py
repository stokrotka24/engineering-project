from rest_framework import generics
from rest_framework.permissions import AllowAny


from authorization.models import User
from authorization.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
