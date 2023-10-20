from django.db import models
from django.contrib.auth.models import User

class FamillyModel (models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)