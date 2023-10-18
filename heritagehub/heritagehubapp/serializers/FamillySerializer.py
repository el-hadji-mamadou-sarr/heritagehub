from rest_framework import serializers
from heritagehub.heritagehubapp.models import FamillyModel
from .PersonSerializer import PersonSerializer

class FamillySerializer(serializers.HyperlinkedModelSerializer):
    
    persons = PersonSerializer(many=True, read_only=True)
    class Meta:
        model = FamillyModel
        fields = ('id','created_by', 'persons')