from django.db import models
from .PersonModel import PersonModel
from django.contrib.auth.models import User


class EventModel (models.Model):
    event_name = models.CharField(max_length=255, blank=False, null=False)
    person_id = models.ForeignKey(PersonModel,related_name='events', on_delete=models.CASCADE, blank=False, null=False)
    event_type = models.CharField(max_length=255, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)