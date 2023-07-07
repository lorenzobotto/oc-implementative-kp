from django.urls import path
from .views import recursive_knapsack
from .views import dinamic_knapsack_matrix
from .views import dinamic_knapsack_single_list

urlpatterns = [
    path('recursive_knapsack', recursive_knapsack),
    path('dinamic_knapsack_matrix', dinamic_knapsack_matrix),
    path('dinamic_knapsack_single_list', dinamic_knapsack_single_list)
]