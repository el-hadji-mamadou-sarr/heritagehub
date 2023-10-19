from rest_framework import serializers
from heritagehub.heritagehubapp.models import MarriageModel
from .PersonSerializer import PersonSerializer


class MarriageSerializer(serializers.HyperlinkedModelSerializer):
    children = PersonSerializer(many=True, read_only=True)
    class Meta:
        model = MarriageModel
        fields = ('id','husband_id', 'wife_id','marriage_date','devorced_at', 'children', 'created_by')