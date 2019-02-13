from django.core import serializers
from django.http import JsonResponse

# Create your views here.
def endpoint(request):
    return JsonResponse({'message': 'hello world!'})
