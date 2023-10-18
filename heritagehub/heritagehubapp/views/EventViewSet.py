from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import EventModel
from heritagehub.heritagehubapp.serializers.EventSerializer import EventSerializer

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
   
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action =='list':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]

    def create(self, request, *args, **kwargs):
        if request.data['event_type'].lower() in EVENT_TYPES:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":" this event type does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)
   