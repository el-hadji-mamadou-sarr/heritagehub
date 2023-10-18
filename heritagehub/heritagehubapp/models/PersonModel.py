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
    birth_date = models.DateField()
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    death_date = models.DateField()
    death_place = models.CharField(max_length=255)
    father_id = models.IntegerField()
    mother_id = models.IntegerField()
    familly_id = models.ForeignKey(FamillyModel,related_name='persons', on_delete=models.CASCADE, blank=False)
    child_from_marriage = models.ForeignKey(MarriageModel,related_name='children', on_delete=models.CASCADE)
    created_by = models.IntegerField()
    
    
    

   
