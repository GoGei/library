from rest_framework import routers
from Api.v3.Author.views import AuthorViewSet
from Api.v3.Book.views import BookViewSet
from Api.v3.Category.views import CategoryViewSet
from Api.v3.User.views import UserViewSet
from Api.v3.Profile.views import ProfileViewSet

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'books', BookViewSet, basename='books')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'users', UserViewSet, basename='users')
router.register(r'profiles', ProfileViewSet, basename='profiles')

urlpatterns = router.urls
