from django.db import models
from django.contrib.auth.models import User

class MarriageModel (models.Model):
    husband_id = models.IntegerField(blank=False, null=False)
    wife_id = models.IntegerField(blank=False, null=False)
    marriage_date = models.DateField(blank=True, null=True)
    devorced_at = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)