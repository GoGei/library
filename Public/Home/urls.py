from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.library_home_view, name='library-home')
]