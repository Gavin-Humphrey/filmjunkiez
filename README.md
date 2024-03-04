![Logo](static/img/film_junkiez_logo.png)


<details>
<summary><strong>Table of Contents</strong></summary>

- [FilmJunkiez](#filmjunkiez):
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation and Launch](#installation-and-launch)
  - [Unit Tests](#unit-tests)
  - [CI/CD (Continuous Integration and Continuous Deployment)](#cicd-continuous-integration-and-continuous-deployment)
    - [CircleCI](#circleci)
    - [Sentry](#sentry)
    - [Cloudinary](#cloudinary)
  - [Deployment](#deployment)
  - [Author](#author)

</details>


## FilmJunkiez

FilmJunkiez is a streaming application where users can upload, view, and review films. Security measures are implemented to ensure user authentication and authorization. Users must follow specific steps to review/comment on films and gain permission to upload films.

### Features

- Users can upload, view, and review films.
- Security measures include password validation, unique email requirements, and email verification.
- Users must follow hosts and evaluate films to review/comment.
- Users must request permission to become hosts to upload films.

### Prerequisites

Ensure you have the following installed before proceeding:

- [Git](https://git-scm.com/)
- [Sentry](https://sentry.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Cloudinary](https://cloudinary.com/)
- [Docker](https://www.docker.com/)
- [CircleCI](https://circleci.com/)
- [Heroku](https://www.heroku.com/)

### Installation and Launch

1. Install Python.
2. Clone the repository:

   ```bash
   git clone https://github.com/Gavin-Humphrey/filmjunkiez.git
<strong>Create and activate a virtual environment:</strong><br>
python -m venv env<br><br>
<strong>macOS/Linux:</strong><br>
source env/bin/activate  <br><br>
<strong>Windows:</strong><br>
env\scripts\activate.bat<br><br> 
<strong>Install required packages:</strong><br>
pip install -r requirements.txt<br><br>
<strong>Migrate the database:</strong><br>
python manage.py makemigrations<br>
python manage.py migrate<br><br>
<strong>Launch the server:</strong><br>
python manage.py runserver,<br>
Access the application at http://127.0.0.1:8000

<strong>Unit Tests</strong><br>
Run unit tests using Pytest:<br>
pytest<br>

CI/CD (Continuous Integration and Continuous Deployment)
<details>
<summary><strong>CircleCI</strong></summary>
Follow these steps to configure CircleCI:

Create a CircleCI account and connect your GitHub account.
Create a new project and select your GitHub repository.
Add the required environment variables to the CircleCI project settings:  
DOCKER_USERNAME: Your Docker Hub username  
DOCKER_LOGIN: Your Docker Hub login email  
HEROKU_APP_NAME: The name of your Heroku application  
HEROKU_TOKEN: Your Heroku API key  
Push a new commit to your repository to trigger a new build on CircleCI.

</details>

<details>
<summary><strong>Sentry</strong></summary>
This application uses Sentry for error tracking. To configure Sentry:

Create a Sentry account and create a new project.

Add the SENTRY_DSN environment variable to your project's .env file.

<strong>Install the Sentry SDK Python package:</strong>

pip install sentry-sdk
Add the generated code to the settings.py file.

</details>

<details>
<summary><strong>Cloudinary Configuration</strong></summary>
To use Cloudinary for image/video storage and manipulation, you need to set up Cloudinary credentials in your Django application:
  
  [Sign up](https://cloudinary.com/) for a Cloudinary account if you haven't already.
  Obtain your Cloudinary API credentials (Cloud name, API Key, API Secret).
  Set the following environment variables in your environment (local development, CI/CD):<br>
  
    - CLOUDINARY_CLOUD_NAME: Your Cloudinary cloud name  
    - CLOUDINARY_API_KEY: Your Cloudinary API key  
    - CLOUDINARY_API_SECRET: Your Cloudinary API secret  
  
</details><br>

<strong>Deployment</strong><br>

This app is deployed on Heroku at https://film-junkiez-be8d3d00a54d.herokuapp.com/.

<strong>Author</strong>
Gavin Humphrey

<small>All rights reserved.</small><br><br>


********* Version française ********<br><br>

<details>
<summary><strong>Table des matières</strong></summary>

- [FilmJunkiez](#filmjunkiez):
  - [Fonctionnalités](#fonctionnalités)
  - [Prérequis](#prérequis)
  - [Installation et lancement](#installation-et-lancement)
  - [Tests unitaires](#tests-unitaires)
  - [CI/CD (Intégration continue et déploiement continu)](#cicd-intégration-continue-et-déploiement-continu)
    - [CircleCI](#circleci)
    - [Sentry](#sentry)
    - [Cloudinary](#cloudinary)
  - [Déploiement](#déploiement)
  - [Auteur](#auteur)

</details>


## FilmJunkiez

FilmJunkiez est une application de streaming où les utilisateurs peuvent télécharger, visionner et commenter des films. Des mesures de sécurité sont mises en œuvre pour garantir l'authentification et l'autorisation des utilisateurs. Ces derniers doivent suivre des étapes spécifiques pour rédiger des critiques/commentaires sur les films et obtenir l'autorisation d'en télécharger.

### Fonctionnalités

- Les utilisateurs peuvent télécharger, visionner et commenter des films.
- Les mesures de sécurité comprennent la validation des mots de passe, l'obligation d'utiliser des adresses e-mail uniques et la vérification des adresses e-mail.
- Les utilisateurs doivent suivre les hôtes et évaluer les films pour pouvoir rédiger des critiques/commentaires.
- Les utilisateurs doivent demander la permission de devenir des hôtes pour pouvoir télécharger des films.

### Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- [Git](https://git-scm.com/)
- [Sentry](https://sentry.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Cloudinary](https://cloudinary.com/)
- [Docker](https://www.docker.com/)
- [CircleCI](https://circleci.com/)
- [Heroku](https://www.heroku.com/)

### Installation et lancement

1. Installez Python.
2. Clonez le dépôt :

   ```bash
   git clone https://github.com/Gavin-Humphrey/filmjunkiez.git
<strong>Créez et activez un environnement virtuel :</strong><br>
python -m venv env<br><br>
<strong>macOS/Linux :</strong><br>
source env/bin/activate <br>  

<strong>Windows :</strong><br>
env\scripts\activate.bat <br><br> 
<strong>Installez les packages requis :</strong><br>
pip install -r requirements.txt<br><br>
<strong>Migrez la base de données :</strong><br>
python manage.py makemigrations<br>
python manage.py migrate<br><br>
<strong>Lancez le serveur :</strong><br>
python manage.py runserver<br>
Accédez à l'application à l'adresse http://127.0.0.1:8000

<strong>Tests unitaires</strong><br>
Exécutez les tests unitaires à l'aide de Pytest :<br>
pytest<br><br>
<strong>CI/CD (Intégration continue et déploiement continu)</strong>
<details>
<summary><strong>CircleCI</strong></summary>
Suivez ces étapes pour configurer CircleCI :

Créez un compte CircleCI et connectez votre compte GitHub.
Créez un nouveau projet et sélectionnez votre dépôt GitHub.
Ajoutez les variables d'environnement requises aux paramètres du projet CircleCI :<br>
DOCKER_USERNAME : Votre nom d'utilisateur Docker Hub  
DOCKER_LOGIN : Votre adresse e-mail de connexion Docker Hub  
HEROKU_APP_NAME : Le nom de votre application Heroku  
HEROKU_TOKEN : Votre clé API Heroku  
Poussez un nouveau commit à votre dépôt pour déclencher une nouvelle construction sur CircleCI.
</details>
<details>
<summary><strong>Sentry</strong></summary>
Ce projet utilise Sentry pour le suivi des erreurs. Pour configurer Sentry :

Créez un compte Sentry et créez un nouveau projet.

Ajoutez la variable d'environnement SENTRY_DSN au fichier .env de votre projet.

Installez le package Python Sentry SDK :

pip install sentry-sdk
Ajoutez le code généré au fichier settings.py.

</details>

<details>
<summary><strong>Configuration de Cloudinary</summary></strong>
Pour utiliser Cloudinary pour le stockage et la manipulation d'images/vidéos, vous devez configurer les identifiants Cloudinary dans votre application Django :

  [Inscrivez-vous](https://cloudinary.com/) pour un compte Cloudinary si ce n'est pas déjà fait.
  Obtenez vos identifiants API Cloudinary (nom du cloud, clé API, secret API).
  Définissez les variables d'environnement suivantes dans votre environnement (développement local, CI/CD) :<br>

    - CLOUDINARY_CLOUD_NAME : Le nom de votre cloud Cloudinary    
    - CLOUDINARY_API_KEY : Votre clé API Cloudinary    
    - CLOUDINARY_API_SECRET : Votre secret API Cloudinary
  
</details><br>

<strong>Déploiement</strong><br>
Le projet est déployé sur Heroku à l'adresse https://film-junkiez-be8d3d00a54d.herokuapp.com/.<br><br>
<strong>Auteur</strong>
Gavin Humphrey

<small>Tous droits réservés.</small>
