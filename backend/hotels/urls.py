from django.urls import path

from hotels import views

urlpatterns = [
    path('hotels/', views.HotelView.as_view()),
    path('hotels/<pk>', views.HotelDetailsView.as_view()),
    path('create_review/', views.CreateReviewView.as_view()),
    path('reviews/', views.ReviewsView.as_view())
]

