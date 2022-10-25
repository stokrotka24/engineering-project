from django.urls import path

from hotels import views

urlpatterns = [
    path('hotels/', views.HotelView.as_view()),
    path('hotels/<pk>', views.HotelDetailsView.as_view()),
    path('create_review/', views.CreateReviewView.as_view()),
    path('hotel_reviews/', views.HotelReviewsView.as_view()),
    path('user_reviews/', views.UserReviewsView.as_view()),
    path('delete_review/<int:pk>', views.DeleteReviewView.as_view())
]

