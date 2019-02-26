from django.core import serializers  # noqa
from django.http import JsonResponse


def endpoint(request):
    return JsonResponse({'message': 'hello world!'})
