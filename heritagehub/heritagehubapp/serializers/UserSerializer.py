from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .FamillySerializer import FamillySerializer
from .EventSerializer import EventSerializer
from .MarriageSerializer import MarriageSerializer
from .PersonSerializer import PersonSerializer
from .RelationSerializer import RelationSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    famillies = FamillySerializer(many=True, read_only=True)
    events = EventSerializer(many=True, read_only=True)
    marriages = MarriageSerializer(many=True, read_only=True)
    persons = PersonSerializer(many=True, read_only=True)
    relations = RelationSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'famillies',
                  'events', 'marriages', 'persons', 'relations')

    def __init__(self, *args, **kwargs):
        # Pass the 'request' from the kwargs to the context
        request = kwargs.pop('context', {}).get('request')
        super(UserSerializer, self).__init__(
            *args, **kwargs, context={'request': request})
