from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import FamillyModel
from heritagehub.heritagehubapp.serializers.FamillySerializer import FamillySerializer
from rest_framework.generics import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class FamillyViewSet(viewsets.ModelViewSet):
   
    queryset = FamillyModel.objects.all().order_by('id')
    serializer_class = FamillySerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action =='list' or self.action == 'retrieve':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]

    @swagger_auto_schema(
        operation_description='Create a post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'created_by': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the user who is creating the post',
                    read_only=True
                )
            }
        ),
        responses={201: 'Post created', 400: 'Bad Request'},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={'created_by':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @swagger_auto_schema(
        operation_description='Retrieve a post',
        responses={200: 'Post retrieved', 404: 'Not Found'},
    )
    def retrieve(self, request, *args, **kwargs):
        familly_id = kwargs.get('pk')
        familly = get_object_or_404(FamillyModel, pk=familly_id)

        serializer = self.get_serializer(familly)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Partial update a post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'field_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Description of the field being updated'
                ),
            }
        ),
        responses={200: 'Post updated', 400: 'Bad Request', 401: 'Unauthorized'},
    )
    def partial_update(self, request, *args, **kwargs):
        
        familly_id = kwargs['pk']
        familly = get_object_or_404(FamillyModel, pk=familly_id)
   
        if self.request.user.id == familly.created_by:
           
            serializer = self.get_serializer(familly, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description='Delete a post',
        responses={200: 'Post deleted', 401: 'Unauthorized'},
    )
    def destroy(self, request, *args, **kwargs):
        familly_id = kwargs['pk']
        familly = get_object_or_404(FamillyModel, pk=familly_id)
        if self.request.user.id == familly.created_by:
            familly.delete()
            return Response( status=status.HTTP_200_OK)
        else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)