from rest_framework import routers
from Api.v1.Users.views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = router_v1.urls
urlpatterns += [

]
