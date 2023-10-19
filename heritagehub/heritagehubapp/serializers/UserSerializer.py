from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .FamillySerializer import FamillySerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    famillies = FamillySerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'famillies']