from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import json

# Create your views here.
@api_view(['POST'])
def first_algorithm(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['name']
    print(content)
    return JsonResponse({'message': 'Hello, World! This is the first algorithm!'})