from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import FamillyModel
from heritagehub.heritagehubapp.serializers.FamillySerializer import FamillySerializer
from rest_framework.generics import get_object_or_404
class FamillyViewSet(viewsets.ModelViewSet):
   
    queryset = FamillyModel.objects.all()
    serializer_class = FamillySerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action =='list' or self.action == 'retrieve':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={'created_by':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        familly_id = kwargs.get('pk')
        familly = get_object_or_404(FamillyModel, pk=familly_id)

        serializer = self.get_serializer(familly)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


    def destroy(self, request, *args, **kwargs):
        familly_id = kwargs['pk']
        familly = get_object_or_404(FamillyModel, pk=familly_id)
        if self.request.user.id == familly.created_by:
            familly.delete()
            return Response( status=status.HTTP_200_OK)
        else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)