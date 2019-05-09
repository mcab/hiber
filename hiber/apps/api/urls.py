from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
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

router = DefaultRouter(trailing_slash=False)
router.register(r'bats', views.BatViewSet)
router.register(r'houses', views.HouseViewSet)

v1_urlpatterns = [
    path('docs/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    url('^', include(router.urls)),
]

# This is to let drf_yasg auto-generate the route while excluding
# other routes from being generated.
urlpatterns = [url(r'api/v1/', include(v1_urlpatterns))]
