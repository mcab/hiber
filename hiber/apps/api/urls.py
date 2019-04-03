from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bat House API",
        default_version="v1",
        description="API to interact with bat house monitoring",
    ),
    urlconf='hiber.apps.api.urls',
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

router = DefaultRouter()
router.register(r'bats', views.BatViewSet)
router.register(r'houses', views.HouseViewSet)

features_router = routers.NestedDefaultRouter(
    router, r'houses', lookup='house')
features_router.register(
    r'environment',
    views.HouseEnvironmentFeaturesViewSet,
    basename='house-environment')
features_router.register(
    r'physical', views.HousePhysicalFeaturesViewSet, basename='house-physical')
features_router.register(
    r'observations', views.ObservationViewSet, basename='house-observations')

v1_urlpatterns = [
    path(
        'docs/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    url('^', include(router.urls)),
    url('^', include(features_router.urls)),
]

# This is to let drf_yasg auto-generate the route while excluding
# other routes from being generated.
urlpatterns = [url(r'api/v1/', include(v1_urlpatterns))]
