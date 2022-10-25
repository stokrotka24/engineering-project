from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authorization.views import RegisterView, ChangePasswordView, AccountInfoView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password/<int:pk>', ChangePasswordView.as_view(), name='change_password'),
    path('account_info/', AccountInfoView.as_view(), name='account_info')
]
