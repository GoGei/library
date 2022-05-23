from django.conf.urls import url
from .schemas import schema_view_v1, schema_view_v2

urlpatterns = [
    url(r'^v1/swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json-v1'),
    url(r'^v1/swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-v1'),
    url(r'^v1/redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),

    url(r'^v2/swagger(?P<format>\.json|\.yaml)$', schema_view_v2.without_ui(cache_timeout=0), name='schema-json-v2'),
    url(r'^v2/swagger/$', schema_view_v2.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-v2'),
    url(r'^v2/redoc/$', schema_view_v2.with_ui('redoc', cache_timeout=0), name='schema-redoc-v2'),
]

