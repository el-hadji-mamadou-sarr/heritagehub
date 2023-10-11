from rest_framework import serializers
from .models import usersModel
from .serializers import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = usersModel
        fields = ('id','nom', 'prenom', 'age','date_naissance', 'lieu_naissance','date_de_deces',
                  'lieu_de_deces','created_at','updated_at')
