from django.db import models
from .PersonModel import PersonModel

class EventModel (models.Model):
    event_name = models.CharField(max_length=255)
    person_id = models.ForeignKey(PersonModel,related_name='events', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=255)