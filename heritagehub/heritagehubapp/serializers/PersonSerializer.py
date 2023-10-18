from rest_framework import serializers
from heritagehub.heritagehubapp.models import PersonModel
from heritagehub.heritagehubapp.models import FamillyModel
from heritagehub.heritagehubapp.models import MarriageModel
from .EventSerializer import EventSerializer

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    familly_id = serializers.PrimaryKeyRelatedField(queryset=FamillyModel.objects.all(), allow_null=True)
    child_from_marriage = serializers.PrimaryKeyRelatedField(queryset=MarriageModel.objects.all(), allow_null=True)
    events = EventSerializer(many=True, read_only=True)
    class Meta:
        model = PersonModel
        fields = ('id','first_name', 'last_name', 'birth_date','created_at',
                  'updated_at','death_date','death_place','father_id',
                  'mother_id','familly_id','child_from_marriage','created_by','events')
           