from django.db import models
from django.contrib.auth.models import User


class MarriageModel (models.Model):
    husband_id = models.ForeignKey(
        'PersonModel', related_name='husbands', on_delete=models.CASCADE, blank=False, null=False)
    wife_id = models.ForeignKey(
        'PersonModel', related_name='wifes', on_delete=models.CASCADE, blank=False, null=False)
    marriage_date = models.DateField(blank=True, null=True)
    devorced_at = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
