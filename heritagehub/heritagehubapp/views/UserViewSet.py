from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest, IsAnonymeUser, IsSuperAdmin
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.serializers.UserSerializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def get_permissions(self):
        if self.action == 'create':
            permission_class = [IsAnonymeUser]
        else:
            permission_class = [IsSuperAdmin]

        return [permission() for permission in permission_class]

    @swagger_auto_schema(
        operation_description='Create a user with JWT token generation',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Username of the user',
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Email of the user',
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Password of the user',
                )
            }
        ),
        responses={201: 'User created with JWT tokens', 400: 'Bad Request'},
    )
    def create(self, request, *args, **kwargs):

        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        # Check if a user with the same username already exists
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)
        user = User.objects.create(
            username=username, password=hashed_password, email=email)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response_data = {
            'user_id': user.id,
            'username': user.username,
            'access_token': access_token,
            'refresh_token': str(refresh),
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description='Retrieve a user',
        responses={200: 'user retrieved',
                   404: 'Not Found', 403: 'Forbidden'},
    )
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
