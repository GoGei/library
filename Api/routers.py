from rest_framework import routers
from Api.v1.Author.views import AuthorViewSet
from Api.v1.Book.views import BookViewSet
from Api.v1.Category.views import CategoryViewSet
from Api.v1.Favourite.views import FavouriteViewSet
from Api.v1.Like.views import LikeViewSet
from Api.v1.Users.views import UserViewSet
from Api.v1.Profile.views import ProfileViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'authors', AuthorViewSet, basename='authors')
router_v1.register(r'books', BookViewSet, basename='books')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'favourite', FavouriteViewSet, basename='favourite')
router_v1.register(r'like', LikeViewSet, basename='like')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = router_v1.urls
urlpatterns += [

]
