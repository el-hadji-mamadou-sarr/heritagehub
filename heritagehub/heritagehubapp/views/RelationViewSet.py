from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import RelationModel
from heritagehub.heritagehubapp.serializers.RelationSerializer import RelationSerializer

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
    "cousin",
    "cousine"]

class RelationViewSet(viewsets.ModelViewSet):
   
    queryset = RelationModel.objects.all()
    serializer_class = RelationSerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action =='list':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]

    def create(self, request, *args, **kwargs):
        if request.data['relation_type'].lower() in RELATION_TYPES:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":" this relation type does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)
   