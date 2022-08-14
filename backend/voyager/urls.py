from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from voyager import views

urlpatterns = [
    path('hello/', views.Hello.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

