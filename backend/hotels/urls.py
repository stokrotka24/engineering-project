from django.urls import path

from hotels import views

urlpatterns = [
    path('hotels/', views.HotelView.as_view())
]

