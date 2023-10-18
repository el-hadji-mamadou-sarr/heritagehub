from rest_framework import serializers
from heritagehub.heritagehubapp.models import EventModel
from heritagehub.heritagehubapp.models import PersonModel


class EventSerializer(serializers.HyperlinkedModelSerializer):
    person_id = serializers.PrimaryKeyRelatedField(queryset=PersonModel.objects.all())
    class Meta:
        model = EventModel
        fields = ('id','event_name', 'person_id','event_type')