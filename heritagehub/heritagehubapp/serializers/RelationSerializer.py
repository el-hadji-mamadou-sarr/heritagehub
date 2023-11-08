from rest_framework import serializers
from heritagehub.heritagehubapp.models import RelationModel
from heritagehub.heritagehubapp.models import PersonModel
from django.contrib.auth.models import User

class RelationSerializer(serializers.HyperlinkedModelSerializer):
    person_id = serializers.PrimaryKeyRelatedField(
        queryset=PersonModel.objects.all())
    other_person_id = serializers.PrimaryKeyRelatedField(
        queryset=PersonModel.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    other_person = serializers.SerializerMethodField()
    class Meta:
        model = RelationModel
        fields = ('id', 'person_id', 'other_person_id',
                  'relation_type', 'created_by', 'other_person')

    def get_other_person(self, obj):
        if obj.other_person_id:
            from .PersonSerializer import PersonSerializer 
            return PersonSerializer(obj.other_person_id).data
        return None