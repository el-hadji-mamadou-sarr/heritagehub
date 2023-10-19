from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest,CanCreateUser,CanListUsers
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.serializers.UserSerializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
  
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]
    
    def get_permissions(self):
        if self.action =='create':
            permission_class = [CanCreateUser]
        
        if self.action == 'list':
            permission_class = [CanListUsers]

        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]
    
    def create(self, request, *args, **kwargs):

        username = request.data['username']

        # Check if a user with the same username already exists
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Get the user object after creating it
        user = User.objects.get(username=serializer.data['username'])
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
        