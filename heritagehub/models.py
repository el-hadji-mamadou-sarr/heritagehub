
from django.db import models

class users(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.TextField()
    age = models.IntegerField()


    def __str__(self):
        return self.nom