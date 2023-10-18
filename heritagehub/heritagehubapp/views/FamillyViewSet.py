from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.models import FamillyModel
from heritagehub.heritagehubapp.serializers.FamillySerializer import FamillySerializer
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.permissions import IsGetRequest

class FamillyViewSet(viewsets.ModelViewSet):
   
    queryset = FamillyModel.objects.all()
    serializer_class = FamillySerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action =='list':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]

    def create(self, request, *args, **kwargs):
            print(self.request.user.id)
            serializer = self.get_serializer(data={'created_by':self.request.user.id})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
   