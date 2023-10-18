from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .MarriageModel import MarriageModel
from .FamillyModel import FamillyModel

def get_default_admin():
    user = User.objects.get()[0]
    return user.id

class PersonModel (models.Model):   
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    death_date = models.DateField(blank=True, null=True)
    death_place = models.CharField(max_length=255, blank=True)
    father_id = models.IntegerField(blank=True, null=True)
    mother_id = models.IntegerField(blank=True, null=True)
    familly_id = models.ForeignKey(FamillyModel,related_name='persons', on_delete=models.CASCADE, blank=True, null=True)
    child_from_marriage = models.ForeignKey(MarriageModel,related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.IntegerField()
    
    
    

   
