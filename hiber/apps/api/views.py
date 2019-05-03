from django.http import HttpResponseServerError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from ..bathouse.models import (Bat, House, HouseEnvironmentFeatures,
                               HousePhysicalFeatures, Observation)
from .permissions import (IsOwnerAndAuthenticated)
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

    def get_queryset(self, *args, **kwargs):
        return House.objects.all().filter(watcher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(watcher=self.request.user)

    @action(
        detail=True,
        methods=['get', 'post'],
        permission_classes=[IsOwnerAndAuthenticated])
    def environment(self, request, pk=None):
        """
        Returns a list of all the environment features
        the house has
        """
        house = self.get_object()
        if (request.method == "GET"):
            ef = HouseEnvironmentFeatures.objects.all().filter(house=house)
            data = [
                HouseEnvironmentFeaturesSerializer(feature).data
                for feature in ef
            ]
            return Response({
                "count": len(ef),
                "results": data
            },
                            status=status.HTTP_200_OK)
        elif (request.method == "POST"):
            data = request.data
            data["house_id"] = house.id
            record = HouseEnvironmentFeatures(**data)
            record.save()
            return Response(
                HouseEnvironmentFeaturesSerializer(record).data,
                status=status.HTTP_201_CREATED)
        return HttpResponseServerError()

    @action(
        detail=True,
        methods=['get', 'post'],
        permission_classes=[IsOwnerAndAuthenticated])
    def physical(self, request, pk=None):
        """
        Returns a list of all the physical features
        the house has
        """
        house = self.get_object()
        if (request.method == "GET"):
            pf = HousePhysicalFeatures.objects.all().filter(house=house)
            data = [
                HousePhysicalFeaturesSerializer(feature).data for feature in pf
            ]
            return Response({
                "count": len(pf),
                "results": data
            },
                            status=status.HTTP_200_OK)
        elif (request.method == "POST"):
            data = request.data
            data["house_id"] = house.id
            record = HousePhysicalFeatures(**data)
            record.save()
            return Response(
                HousePhysicalFeaturesSerializer(record).data,
                status=status.HTTP_201_CREATED)
        return HttpResponseServerError()

    @action(
        detail=True,
        methods=['get', 'post'],
        permission_classes=[IsOwnerAndAuthenticated])
    def observations(self, request, pk=None):
        """
        Returns a list of all the observations the house has
        """
        house = self.get_object()
        if (request.method == "GET"):
            ob = Observation.objects.all().filter(house=house)
            data = [ObservationSerializer(feature).data for feature in ob]
            return Response({
                "count": len(ob),
                "results": data
            },
                            status=status.HTTP_200_OK)
        elif (request.method == "POST"):
            data = request.data
            data["house_id"] = house.id
            record = Observation(**data)
            record.save()
            return Response(
                ObservationSerializer(record).data,
                status=status.HTTP_201_CREATED)
        return HttpResponseServerError()


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
