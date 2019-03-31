from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from ..bathouse.models import Bat
from .serializers import BatSerializer, UserSerializer
from rest_framework.views import APIView


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bat.objects.all()
    serializer_class = BatSerializer


class AuthView(APIView):
    """
    Return the URLs from the authentication portion of the application.
    """

    def get(self, request, *args, **kwargs):
        endpoints = [
            'user', 'user-create', 'user-delete', 'user-activate',
            'user-activate-resend', 'set-password', 'reset-password',
            'reset-password-confirm', 'token-create', 'token-destroy', 'login',
            'logout'
        ]
        return Response(
            {k: request.build_absolute_uri(reverse(k))
             for k in endpoints})
