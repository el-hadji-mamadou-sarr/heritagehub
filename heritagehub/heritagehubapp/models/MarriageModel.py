from django.db import models

class MarriageModel (models.Model):
    husband_id = models.IntegerField(blank=False, null=False)
    wife_id = models.IntegerField(blank=False, null=False)
    marriage_date = models.DateField(blank=True, null=True)
    devorced_at = models.DateField(blank=True, null=True)
    created_by = models.IntegerField()