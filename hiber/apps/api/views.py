from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from ..bathouse.models import (Bat, House, HouseEnvironmentFeatures,
                               HousePhysicalFeatures, Observation)
from .serializers import (
    BatSerializer, HouseSerializer, HouseEnvironmentFeaturesSerializer,
    HousePhysicalFeaturesSerializer, ObservationSerializer)


class BatViewSet(viewsets.ReadOnlyModelViewSet):
    model = Bat
    queryset = Bat.objects.all()
    serializer_class = BatSerializer


class HouseViewSet(viewsets.ModelViewSet):
    model = House
    permission_classes = (IsAuthenticated, )
    queryset = House.objects.all()
    serializer_class = HouseSerializer

    def perform_create(self, serializer):
        serializer.save(watcher=self.request.user)


class HouseEnvironmentFeaturesViewSet(viewsets.ModelViewSet):
    model = HouseEnvironmentFeatures
    permission_classes = (IsAuthenticated, )
    queryset = HouseEnvironmentFeatures.objects.all()
    serializer_class = HouseEnvironmentFeaturesSerializer

    def get_queryset(self):
        return HouseEnvironmentFeatures.objects.filter(
            house=self.kwargs["house_pk"])


class HousePhysicalFeaturesViewSet(viewsets.ModelViewSet):
    model = HousePhysicalFeatures
    permission_classes = (IsAuthenticated, )
    queryset = HousePhysicalFeatures.objects.all()
    serializer_class = HousePhysicalFeaturesSerializer

    def get_queryset(self):
        return HousePhysicalFeatures.objects.filter(
            house=self.kwargs["house_pk"])


class ObservationViewSet(viewsets.ModelViewSet):
    model = Observation
    permission_classes = (IsAuthenticated, )
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer

    def get_queryset(self):
        return Observation.objects.filter(house=self.kwargs["house_pk"])


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
