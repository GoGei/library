from django.conf.urls import url
from rest_framework import routers
from Api.v2.Author.views import AuthorViewSet
from Api.v2.Book.views import BookViewSet
from Api.v2.Category.views import CategoryViewSet
from Api.v2.User.views import ProfileView

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'books', BookViewSet, basename='books')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = router.urls
urlpatterns += [
    url(r'^profile/$', ProfileView.as_view(), name='profile')
]
