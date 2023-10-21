from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import PersonModel
from heritagehub.heritagehubapp.serializers.PersonSerializer import PersonSerializer
from rest_framework.generics import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class PersonViewSet(viewsets.ModelViewSet):

    queryset = PersonModel.objects.all().order_by('id')
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]

    @swagger_auto_schema(
        operation_description='Create a person',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='First name of the person',
                ),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Last name of the person',
                ),
                'birth_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Date of birth of the person',
                ),
            }
        ),
        responses={201: 'Person created', 400: 'Bad Request'},
    )
    def create(self, request, *args, **kwargs):
        person_data = request.data.copy()
        person_data['created_by'] = self.request.user.id

        serializer = self.get_serializer(data=person_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description='Retrieve a person',
        responses={200: 'Person retrieved', 404: 'Not Found'},
    )
    def retrieve(self, request, *args, **kwargs):
        person_id = kwargs.get('pk')
        person = get_object_or_404(PersonModel, pk=person_id)

        serializer = self.get_serializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Partial update a person',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='First name of the person',
                ),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Last name of the person',
                ),
            }
        ),
        responses={200: 'Person updated',
                   400: 'Bad Request', 401: 'Unauthorized'},
    )
    def partial_update(self, request, *args, **kwargs):
        person_id = kwargs['pk']
        person = get_object_or_404(PersonModel, pk=person_id)

        if self.request.user == person.created_by:
            serializer = self.get_serializer(
                person, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description='Delete a person',
        responses={200: 'Person deleted', 401: 'Unauthorized'},
    )
    def destroy(self, request, *args, **kwargs):
        person_id = kwargs['pk']
        person = get_object_or_404(PersonModel, pk=person_id)
        if self.request.user == person.created_by:
            person.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
