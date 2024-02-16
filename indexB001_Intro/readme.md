# Déploiement de Dash

*Date : 16-02-2024*

***Éditeur : Laurent Reynaud***

#### Étape 1 :

Ajouter la ligne de code suivant dans le fichier principal de python, après avoir instancier la sous-librairie Dash :

> server = app.server

#### Étape 2 :

Lire préalablement ceci : [déployer une application web](https://github.com/thusharabandara/dash-app-render-deployment)

* Il est conseillé de nommer le fichier principal "app.py"
* Pour le fichier requirements.txt : copier les librairies du site GitHub pour déployer une application web -> éviter de mettre des numéros de version
* Ajouter "gunicorn" dans le fichier requirements.txt qui doit-être inclus dans le répertoire ciblé

#### Étape 3 :

Sur github, déployer le dossier ciblé dans un **NOUVEAU** repository

#### Étape 4 :

Sur le site [render](https://dashboard.render.com/), cliquer sur :

- New
- Web Service
- Build and deploy from a Git repository
- À la page suivante, dans le menu en bas "Publig Git Repository", copier l'URL du répertoire ciblé et déposé sur GitHub
- À la page suivante :
  - Name : saisir un nom au hasard qui sera une partie de l'url pour le partage du fichier (ex : lrcompta-NomDossier)
  - Region : Frankfurt (EU Central)
  - Start command -> saisir : gunicorn nomFichierPrincipal:server (exemple gunicorn app:server)
  - Instance Free : Free (pour l'instant)
  - Puis cliquer sur le bouton "Create Web Service"
