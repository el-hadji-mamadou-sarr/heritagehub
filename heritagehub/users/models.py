from django.db import models

# Create your models here.
class usersModel(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.TextField(ax_length=255)
    age = models.IntegerField()
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=255)
    date_de_deces = models.DateField(null=True)
    lieu_de_deces = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.prenom} {self.nom_de_famille}"