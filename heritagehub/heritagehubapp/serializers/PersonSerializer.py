from rest_framework import serializers
from heritagehub.heritagehubapp.models import PersonModel


class PersonSerializer(serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = PersonModel
        fields = ('first_name', 'last_name', 'birth_date','created_at'
                  'updated_at','death_date','death_place','father_id'
                  'mother_id','familly_id','chil_from_marriage','created_by')
           