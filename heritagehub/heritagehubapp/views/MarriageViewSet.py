from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import MarriageModel
from heritagehub.heritagehubapp.serializers.MarriageSerializer import MarriageSerializer

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
    
   