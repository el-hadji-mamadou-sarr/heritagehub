from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .FamillySerializer import FamillySerializer
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    famillies = FamillySerializer(many=True,read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'famillies']