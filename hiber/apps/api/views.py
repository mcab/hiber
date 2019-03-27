from django.contrib.auth.models import User
from rest_framework import viewsets
from ..bathouse.models import Bat
from .serializers import BatSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bat.objects.all()
    serializer_class = BatSerializer
