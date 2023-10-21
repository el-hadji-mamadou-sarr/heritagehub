from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import RelationModel
from heritagehub.heritagehubapp.serializers.RelationSerializer import RelationSerializer
from rest_framework.generics import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

RELATION_TYPES = [
    "pere",
    "mere",
    "fils",
    "fille",
    "frere",
    "soeur",
    "grand-pere",
    "grand-mere",
    "petit-fils",
    "petite-fille",
    "oncle",
    "tante",
    "neveu",
    "niece",
    "ami",
    "cousin",
    "cousine"]


class RelationViewSet(viewsets.ModelViewSet):

    queryset = RelationModel.objects.all().order_by('id')
    serializer_class = RelationSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]

    @swagger_auto_schema(
        operation_description='Create a relation',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'person_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the person',
                ),
                'other_person_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the other person',
                ),
                'relation_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Type of the relation',
                ),
            }
        ),
        responses={201: 'Relation created',
                   400: 'Bad Request', 406: 'Not Acceptable'},
    )
    def create(self, request, *args, **kwargs):
        if request.data['relation_type'].lower() in RELATION_TYPES:
            relation_data = request.data.copy()
            relation_data['created_by'] = self.request.user.id
            serializer = self.get_serializer(data=relation_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": " this relation type does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @swagger_auto_schema(
        operation_description='Retrieve a relation',
        responses={200: 'Relation retrieved', 404: 'Not Found'},
    )
    def retrieve(self, request, *args, **kwargs):
        relation_id = kwargs.get('pk')
        relation = get_object_or_404(RelationModel, pk=relation_id)

        serializer = self.get_serializer(relation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Partial update a relation',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'person_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the person',
                ),
                'other_person_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the other person',
                ),
                'relation_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Type of the relation',
                ),
            }
        ),
        responses={200: 'Relation updated',
                   406: 'Not Acceptable',
                   400: 'Bad Request', 401: 'Unauthorized'},
    )
    def partial_update(self, request, *args, **kwargs):

        relation_id = kwargs['pk']
        relation = get_object_or_404(RelationModel, pk=relation_id)

        if self.request.user == relation.created_by:
            if 'relation_type' in request.data:
                if request.data['relation_type'].lower() not in RELATION_TYPES:
                    return Response({"message": "This relation type does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = self.get_serializer(
                relation, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description='Delete a relation',
        responses={200: 'Relation deleted', 401: 'Unauthorized'},
    )
    def destroy(self, request, *args, **kwargs):
        relation_id = kwargs['pk']
        relation = get_object_or_404(RelationModel, pk=relation_id)
        if self.request.user == relation.created_by:
            relation.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
