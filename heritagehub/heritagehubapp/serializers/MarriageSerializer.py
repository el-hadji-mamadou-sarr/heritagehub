from rest_framework import serializers
from heritagehub.heritagehubapp.models import MarriageModel
from heritagehub.heritagehubapp.models.PersonModel import PersonModel
from .PersonSerializer import PersonSerializer
from django.contrib.auth.models import User


class MarriageSerializer(serializers.HyperlinkedModelSerializer):
    children = PersonSerializer(many=True, read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    husband_id = serializers.PrimaryKeyRelatedField(
        queryset=PersonModel.objects.all())
    wife_id = serializers.PrimaryKeyRelatedField(
        queryset=PersonModel.objects.all())

    class Meta:
        model = MarriageModel
        fields = ('id', 'husband_id', 'wife_id', 'marriage_date',
                  'devorced_at', 'children', 'created_by')
