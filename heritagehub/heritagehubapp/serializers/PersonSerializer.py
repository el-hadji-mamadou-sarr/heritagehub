from rest_framework import serializers
from heritagehub.heritagehubapp.models import PersonModel
from heritagehub.heritagehubapp.models import FamillyModel
from heritagehub.heritagehubapp.models import MarriageModel
from .EventSerializer import EventSerializer
from .RelationSerializer import RelationSerializer
from django.contrib.auth.models import User


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    familly_id = serializers.PrimaryKeyRelatedField(
        queryset=FamillyModel.objects.all(), allow_null=True)
    child_from_marriage = serializers.PrimaryKeyRelatedField(
        queryset=MarriageModel.objects.all(), allow_null=True)
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    father_id = serializers.PrimaryKeyRelatedField(
        queryset=PersonModel.objects.all(), allow_null=True)
    mother_id = serializers.PrimaryKeyRelatedField(
        queryset=PersonModel.objects.all(), allow_null=True)
    events = EventSerializer(many=True, read_only=True)
    relations = RelationSerializer(many=True, read_only=True)

    class Meta:
        model = PersonModel
        fields = ('id', 'first_name', 'last_name', 'birth_date', 'gender', 'created_at',
                  'updated_at', 'death_date', 'death_place', 'father_id',
                  'mother_id', 'familly_id', 'child_from_marriage', 'created_by', 'events', 'relations')
