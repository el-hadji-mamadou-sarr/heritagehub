from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import MarriageModel
from heritagehub.heritagehubapp.serializers.MarriageSerializer import MarriageSerializer
from rest_framework.generics import get_object_or_404

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        marriage_id = kwargs.get('pk')
        marriage = get_object_or_404(MarriageModel, pk=marriage_id)

        serializer = self.get_serializer(marriage)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


    def destroy(self, request, *args, **kwargs):
        marriage_id = kwargs['pk']
        marriage = get_object_or_404(MarriageModel, pk=marriage_id)
        if self.request.user.id == marriage.created_by:
            marriage.delete()
            return Response( status=status.HTTP_200_OK)
        else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAMarriageModel)
    
   