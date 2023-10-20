from django.db import models
from .PersonModel import PersonModel
from django.contrib.auth.models import User

class RelationModel(models.Model):
    person_id = models.ForeignKey(PersonModel,related_name='relations', on_delete=models.CASCADE, blank=False, null=False)
    other_person_id = models.IntegerField(blank=False, null=False)
    relation_type = models.CharField(max_length=255, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)