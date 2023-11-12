from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import EventModel
from heritagehub.heritagehubapp.serializers.EventSerializer import EventSerializer
from rest_framework.generics import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

EVENT_TYPES = [
    "naissance",
    "enfance",
    "education",
    "relations",
    "emploi",
    "mariage",
    "parentalite",
    "demenagement",
    "pertes",
    "realisations",
    "sante",
    "vieillissement",
    "retraite",
    "mort",
    "annivairsaire"]

class EventViewSet(viewsets.ModelViewSet):

    queryset = EventModel.objects.all().order_by('id')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]

    @swagger_auto_schema(
        operation_description='Create an event',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'event_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Name of the event',
                ),
                'person_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the associated person',
                ),
                'event_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Type of the event',
                ),
            }
        ),
        responses={201: 'Event created',
                   400: 'Bad Request', 406: 'Not Acceptable'},
    )
    def create(self, request, *args, **kwargs):
        if request.data['event_type'].lower() in EVENT_TYPES:
            event_data = request.data.copy()
            event_data['created_by'] = self.request.user.id
            serializer = self.get_serializer(data=event_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": " this event type does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @swagger_auto_schema(
        operation_description='Retrieve an event',
        responses={200: 'Event retrieved', 404: 'Not Found'},
    )
    def retrieve(self, request, *args, **kwargs):
        event_id = kwargs.get('pk')
        event = get_object_or_404(EventModel, pk=event_id)

        serializer = self.get_serializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description='Partial update an event',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'event_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Name of the event',
                ),
                'person_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the associated person',
                ),
                'event_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Type of the event',
                ),
            }
        ),
        responses={200: 'Event updated',
                   406: 'Not Acceptable',
                   400: 'Bad Request', 401: 'Unauthorized'},
    )
    def partial_update(self, request, *args, **kwargs):

        event_id = kwargs['pk']
        event = get_object_or_404(EventModel, pk=event_id)

        if self.request.user == event.created_by:
            if 'relation_type' in request.data:
                if request.data['event_type'].lower() not in EVENT_TYPES:
                    return Response({"message": "This event type does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer = self.get_serializer(
                event, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description='Delete an event',
        responses={200: 'Event deleted', 401: 'Unauthorized'},
    )
    def destroy(self, request, *args, **kwargs):
        event_id = kwargs['pk']
        event = get_object_or_404(EventModel, pk=event_id)
        if self.request.user == event.created_by:
            event.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message": "permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
