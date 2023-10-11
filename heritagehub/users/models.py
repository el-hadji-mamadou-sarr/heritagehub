from django.db import models

# Create your models here.
class users(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.TextField(ax_length=255)
    age = models.IntegerField()
    


    def __str__(self):
        return self.nom