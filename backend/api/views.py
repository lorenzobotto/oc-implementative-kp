from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .algo import Knapsack
import json

# Create your views here.
@api_view(['POST'])
def recursive_knapsack(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    capacity = body['capacity']
    profits = body['profits']
    weights = body['weights']
    knapsack = Knapsack(capacity, profits, weights)
    knapsack.sort_by_ratio()
    content = knapsack.dp1()
    print(content)
    return JsonResponse(content)

@api_view(['POST'])
def dynamic_knapsack_matrix(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    capacity = body['capacity']
    profits = body['profits']
    weights = body['weights']
    knapsack = Knapsack(capacity, profits, weights)
    knapsack.sort_by_ratio()
    content = knapsack.dynamic_knapsack_matrix()
    print(content)
    return JsonResponse(content)

@api_view(['POST'])
def dynamic_knapsack_single_list(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    capacity = body['capacity']
    profits = body['profits']
    weights = body['weights']
    knapsack = Knapsack(capacity, profits, weights)
    knapsack.sort_by_ratio()
    content = knapsack.dynamic_knapsack_single_list()
    print(content)
    return JsonResponse(content)