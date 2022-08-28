from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authorization import views
from authorization.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', views.Hello.as_view())
]
