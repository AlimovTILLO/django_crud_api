from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, RegistrationAPI, LoginAPI, ProductViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]