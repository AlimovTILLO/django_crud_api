from django.contrib.auth.models import User
from .models import Product, User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from knox.models import AuthToken
from .serializers import UserSerializer, ProductSerializer, LoginUserSerializer, CreateUserSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class MediumResultsSetPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'page': self.page.number,
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'data': data
        })

    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardResultsSetPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'page': self.page.number,
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'data': data
        })

    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = MediumResultsSetPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ('name', 'year', 'color')
    # filter_fields = ('name', 'year')
    search_fields = ('name', 'year')

    def get_search_fields(self, view, request):
        if request.query_params.get('name_only'):
            return ['name']
        return super(ProductViewSet, self).get_search_fields(view, request)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user":
            UserSerializer(user, context=self.get_serializer_context()).data,
            "token":
            AuthToken.objects.create(user)[1]
        })


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user":
            UserSerializer(user, context=self.get_serializer_context()).data,
            "token":
            AuthToken.objects.create(user)[1]
        })
