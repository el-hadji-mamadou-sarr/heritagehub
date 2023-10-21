## Présentation du projet

Ce projet a pour but de permettre aux utilisateurs de voir leur arbre généalogique ainsi que les événements qui se sont passés pour
chaque membre de leur famille.

## Fonctionnalités

- Créer un compte utilisateur avec un identifiant unique.
- Se connceter à compte avec son identifiant et son mot de passe.
- se déconnecter de son compte.
- La création d'entités (familles, personnes, événements, marriages, etc) est uniquement réservée aux utilisateurs authentifiés.
- Protection des données utilisateurs: seul le super utilisateur peut lister les utilisateurs et afficher leurs détails.
- La recherche: recherche par non ou par prénom juste ajouter `persons?search=nom_de_la_personne`.oubien son prénom.
- La recherche par username ou par email pour le super utilisateur `users?search=identifiant_de_la_personne`. oubien son email.

## installation du projet

- creér votre environnement `python3 -m venv env `
- activer votre environnement `env/Scripts/activate `
- installer les dépendances de l'application `pip install -r requirements.txt `
- créer une nouvelle migration `python manage.py makemigrations `
- miggrer cette derniére vers la base de donnée `python manage.py migrate `

## Faire les tests unitaires

`python manage.py tests `

## python version

Python 3.11.5
