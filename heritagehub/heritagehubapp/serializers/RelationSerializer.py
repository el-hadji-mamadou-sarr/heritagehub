from rest_framework import serializers
from heritagehub.heritagehubapp.models import RelationModel
from heritagehub.heritagehubapp.models import PersonModel


class RelationSerializer(serializers.HyperlinkedModelSerializer):
    person_id = serializers.PrimaryKeyRelatedField(queryset=PersonModel.objects.all())
    class Meta:
        model = RelationModel
        fields = ('id', 'person_id','other_person_id','relation_type')