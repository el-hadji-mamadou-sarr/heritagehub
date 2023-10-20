from rest_framework import serializers
from heritagehub.heritagehubapp.models import RelationModel
from heritagehub.heritagehubapp.models import PersonModel
from django.contrib.auth.models import User


class RelationSerializer(serializers.HyperlinkedModelSerializer):
    person_id = serializers.PrimaryKeyRelatedField(queryset=PersonModel.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = RelationModel
        fields = ('id', 'person_id','other_person_id','relation_type', 'created_by')