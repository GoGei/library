from django.conf import settings
from django.conf.urls import include, url
from rest_framework import permissions

from Api.v1.routers import router as router_v1
from Api.v2.routers import router as router_v2
from Api.v3.routers import router as router_v3

from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

api_url = '%s://api%s' % (settings.SITE_SCHEME, settings.PARENT_HOST)

if settings.HOST_PORT:
    api_url = '%s://api%s:%s' % (settings.SITE_SCHEME, settings.PARENT_HOST, settings.HOST_PORT)

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Superuser API",
        default_version='v1',
        description='API for superusers with full access to every model',
    ),
    url=api_url,
    patterns=[url(r'^v1/', include((router_v1.urls, 'Api'), namespace='api-v1'))],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_view_v2 = get_schema_view(
    openapi.Info(
        title="User API",
        default_version='v1',
        description='API for users to read data and manage with their profiles',
    ),
    url=api_url,
    patterns=[url(r'^v2/', include((router_v2.urls, 'Api'), namespace='api-v2'))],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_view_v3 = get_schema_view(
    openapi.Info(
        title="Staff API",
        default_version='v1',
        description='API for staff with access to provided model and manage them (with GUI)',
    ),
    url=api_url,
    patterns=[url(r'^v3/', include((router_v3.urls, 'Api'), namespace='api-v3'))],
    public=True,
    permission_classes=(permissions.AllowAny,),
)
