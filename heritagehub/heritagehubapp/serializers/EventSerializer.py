from rest_framework import serializers
from heritagehub.heritagehubapp.models import EventModel
from heritagehub.heritagehubapp.models import PersonModel
from django.contrib.auth.models import User


class EventSerializer(serializers.HyperlinkedModelSerializer):
    person_id = serializers.PrimaryKeyRelatedField(queryset=PersonModel.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = EventModel
        fields = ('id','event_name', 'person_id','event_type','created_by')