from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from ..bathouse.models import Bat
from .serializers import BatSerializer, UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bats':
        reverse('bat-list', request=request, format=format),
        'users':
        reverse('user-list', request=request, format=format),
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bat.objects.all()
    serializer_class = BatSerializer
