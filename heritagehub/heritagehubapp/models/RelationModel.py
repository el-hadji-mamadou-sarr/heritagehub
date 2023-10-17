from django.db import models
from .PersonModel import PersonModel

class RelationModel(models.Model):
    person_id = models.ForeignKey(PersonModel,related_name='relations', on_delete=models.CASCADE)
    other_person_id = models.IntegerField(blank=False)
    relation_type = models.CharField(max_length=255, blank=False)