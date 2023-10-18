from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import PersonModel
from heritagehub.heritagehubapp.serializers.PersonSerializer import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
   
    queryset = PersonModel.objects.all()
    serializer_class = PersonSerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action =='list':
            permission_class = [IsGetRequest]
        else:
            permission_class = [IsAuthenticated]

        return [permission() for permission in permission_class]
    
    def create(self, request, *args, **kwargs):
        # get a copy of the request data
        person_data = request.data.copy()

        #add the created_by field to the object
        person_data['created_by'] = self.request.user.id
        
        serializer = self.get_serializer(data=person_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)