# Déploiement de Dash

*Date : 16-02-2024*

***Éditeur : Laurent Reynaud***

#### Étape 1 :

Ajouter la ligne de code suivant dans le fichier principal de python, après avoir instancier la sous-librairie Dash :

> server = app.server

#### Étape 2 :

Lire préalablement ceci : [déployer une application web](https://github.com/thusharabandara/dash-app-render-deployment)

* Il est conseillé de nommer le fichier principal "app.py"
* La version de la  ****librairie pandas doit être inférieure à 1.6
* Ajouter "gunicorn" dans le fichier requirements.txt qui doit-être inclus dans le répertoire ciblé

#### Étape 3 :

Sur github, déployer le dossier ciblé dans un repository

#### Étape 4 :

Sur le site [render](https://dashboard.render.com/), cliquer sur :

- Nouveau
- Service Web
- Construire et déployer à partir d'un référentiel Git
- Puis récupérer le repertoire Github à partager

Pour la configuration du déploiement du fichier principal sur l'application @, dans la partie "Démarrer la commande", saisir : gunicorn nomFichierPrincipal:server (exemple gunicorn app:server)
