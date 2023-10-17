from rest_framework import serializers
from heritagehubapp.models import PersonModel


class PersonSerializer(serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = PersonModel
        fields = ('first_name', 'last_name')   