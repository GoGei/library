from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    # host('', 'PathToUrls.urls', name='public'),
    # host('api', 'PathToUrls.urls', name='api'),
    # host('admin', 'PathToUrls.urls', name='admin'),
)
