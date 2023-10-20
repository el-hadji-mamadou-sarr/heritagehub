from rest_framework import serializers
from heritagehub.heritagehubapp.models import FamillyModel
from .PersonSerializer import PersonSerializer
from django.contrib.auth.models import User

class FamillySerializer(serializers.HyperlinkedModelSerializer):
    
    persons = PersonSerializer(many=True, read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FamillyModel
        fields = ('id','created_by', 'persons')