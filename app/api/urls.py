from django.conf.urls import include, url
from rest_framework import routers
from .views import UserViewSet, RegistrationAPI, LoginAPI, ProductViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    url('', include(router.urls)),
    url('register/', RegistrationAPI.as_view()),
    url('login/', LoginAPI.as_view()),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]