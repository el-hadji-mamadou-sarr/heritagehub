from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import RelationModel
from heritagehub.heritagehubapp.serializers.RelationSerializer import RelationSerializer
from rest_framework.generics import get_object_or_404
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
        

    def retrieve(self, request, *args, **kwargs):
        relation_id = kwargs.get('pk')
        relation = get_object_or_404(RelationModel, pk=relation_id)

        serializer = self.get_serializer(relation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        
        relation_id = kwargs['pk']
        relation = get_object_or_404(RelationModel, pk=relation_id)
   
        if self.request.user.id == relation.created_by:
           
            serializer = self.get_serializer(relation, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)


    def destroy(self, request, *args, **kwargs):
        relation_id = kwargs['pk']
        relation = get_object_or_404(RelationModel, pk=relation_id)
        if self.request.user.id == relation.created_by:
            relation.delete()
            return Response( status=status.HTTP_200_OK)
        else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
      
   