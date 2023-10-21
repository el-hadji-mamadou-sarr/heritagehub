from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .MarriageModel import MarriageModel
from .FamillyModel import FamillyModel
from django.contrib.auth.models import User


def get_default_admin():
    user = User.objects.get()[0]
    return user.id


class PersonModel (models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, default='male')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    death_date = models.DateField(blank=True, null=True)
    death_place = models.CharField(max_length=255, blank=True)
    father_id = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='fathers_children', blank=True, null=True, default=None)
    mother_id = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='mothers_children', blank=True, null=True, default=None)
    familly_id = models.ForeignKey(FamillyModel,
                                   related_name='persons',
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True,
                                   default=None)
    child_from_marriage = models.ForeignKey(MarriageModel,
                                            related_name='children',
                                            on_delete=models.CASCADE,
                                            blank=True,
                                            null=True,
                                            default=None)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
