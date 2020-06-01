## Techniques-web-INALCO-2020

Correction de l'examen du cours Techniques web (Master 2 - TAL - 2020): Mise en place d'une API REST et d'un Front-end avec Python et Flask. 

`NB:` Cette version est temporaire et peut encore être améliorée (surtout la partie UX et sécurité) 

## Organisation interne 

Le projet est constitué de deux applications web utilisant la librairie Python Flask, routées par un Middleware de bout en bout. 

1- le dossier **cepty**: l'application API REST
2- le dossier **front**: l'application Front-end
3- le fichier **tests.py**: pour les lancer les tests unitaires
4- le fichier **start_app.py**: pour lancer l'application

## Installation

Configurer votre environnement de développement avec **pipenv**. 

    pipenv --python 3.6
    pipenv install
    pipenv shell

## Utilisation

Les deux applications fonctionnent sous un seul serveur partageant une URL. On le lance avec le fichier `start_app.py`. 

    python3 start_app.py


Les URLs d'accès sont les suivants:

- l'API REST: `localhost:5000/api/v0.2`
- l'application front: `localhost:5000`

