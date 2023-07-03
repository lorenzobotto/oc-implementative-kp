from django.urls import path
from .views import first_algorithm

urlpatterns = [
    path('home', first_algorithm)
]