from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import MarriageModel
from heritagehub.heritagehubapp.serializers.MarriageSerializer import MarriageSerializer
from rest_framework.generics import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class MarriageViewSet(viewsets.ModelViewSet):
   
    queryset = MarriageModel.objects.all()
    serializer_class = MarriageSerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action =='list':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]

    @swagger_auto_schema(
        operation_description='Create a marriage',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'husband_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the husband',
                ),
                'wife_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the wife',
                ),
                'marriage_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Date of marriage',
                ),
            }
        ),
        responses={201: 'Marriage created', 400: 'Bad Request'},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        operation_description='Retrieve a marriage',
        responses={200: 'Marriage retrieved', 404: 'Not Found'},
    )
    def retrieve(self, request, *args, **kwargs):
        marriage_id = kwargs.get('pk')
        marriage = get_object_or_404(MarriageModel, pk=marriage_id)

        serializer = self.get_serializer(marriage)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Partial update a marriage',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'husband_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the husband',
                ),
                'wife_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the wife',
                ),
                'marriage_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Date of marriage',
                ),
            }
        ),
        responses={200: 'Marriage updated', 400: 'Bad Request', 401: 'Unauthorized'},
    )
    def partial_update(self, request, *args, **kwargs):
        
        marriage_id = kwargs['pk']
        marriage = get_object_or_404(MarriageModel, pk=marriage_id)
   
        if self.request.user.id == marriage.created_by:
           
            serializer = self.get_serializer(marriage, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description='Delete a marriage',
        responses={200: 'Marriage deleted', 401: 'Unauthorized'},
    )
    def destroy(self, request, *args, **kwargs):
        marriage_id = kwargs['pk']
        marriage = get_object_or_404(MarriageModel, pk=marriage_id)
        if self.request.user.id == marriage.created_by:
            marriage.delete()
            return Response( status=status.HTTP_200_OK)
        else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
    
   