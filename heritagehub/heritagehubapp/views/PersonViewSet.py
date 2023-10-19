from rest_framework import viewsets, status
from rest_framework.response import Response
from heritagehub.heritagehubapp.permissions import IsGetRequest
from rest_framework.permissions import IsAuthenticated
from heritagehub.heritagehubapp.models import PersonModel
from heritagehub.heritagehubapp.serializers.PersonSerializer import PersonSerializer
from rest_framework.generics import get_object_or_404


class PersonViewSet(viewsets.ModelViewSet):
   
    queryset = PersonModel.objects.all()
    serializer_class = PersonSerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.action =='list' or self.action == 'retrieve':
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
  

    def retrieve(self, request, *args, **kwargs):
      person_id = kwargs.get('pk')
      person = get_object_or_404(PersonModel, pk=person_id)

      serializer = self.get_serializer(person)
      return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
         if self.request.user.id == request.data['created_by']:
            person_id = kwargs['pk']
            person = get_object_or_404(PersonModel, pk=person_id)

            serializer = self.get_serializer(person, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
         else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
      if self.request.user.id == request.data['created_by']:
        person_id = kwargs['pk']
        person = get_object_or_404(PersonModel, pk=person_id)

        person.delete()
        return Response( status=status.HTTP_200_OK)
      else:
            return Response({"message":"permission denied"}, status=status.HTTP_401_UNAUTHORIZED)