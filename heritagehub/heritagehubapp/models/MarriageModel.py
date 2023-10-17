from django.db import models

class MarriageModel (models.Model):
    husband_id = models.IntegerField(blank=False)
    wife_id = models.IntegerField(blank=False)
    marriage_date = models.DateField()
    devorced_at = models.DateField()