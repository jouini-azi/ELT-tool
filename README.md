# ELT-tool

# Description

Ce projet est une application de gestion et d’exécution de jobs ETL permettant de charger, traiter et stocker des données à partir de fichiers externes vers une base de données.
L’objectif est de faciliter l’automatisation des traitements de données tout en offrant une interface simple pour l’administration des jobs.

# Objerctifs su projet

- Automatiser les processus ETL
- Centraliser la gestion des jobs
- Assurer le suivi des exécutions
- Simplifier l’utilisation pour les utilisateurs non techniques

# Environnement de travail

- Pour ce projet on a besoin de deux bases de données
- MySQL:
  lien d'installation : https://dev.mysql.com/downloads/mysql/
- MongoDB:
  lien d'installation : https://www.mongodb.com/try/download/compass

# Installation

## Streamlit

- On a besoin d'installer la bibliotheque Streamlit
- Commande pour l'installation:
  pip install streamlit
- verification de l'installation dans le terminal :
  pip show streamlit

## mysql-connector

- On a besoin d'installer la bibliotheque mysql-connector-python
- Commande pour l'installation:
  pip install mysql-connector-python
- verification de l'installation dans le terminal :
  pip show mysql-connector-python

## pymongo

- On a besoin d'installer la bibliotheque pymongo
- Commande pour l'installation:
  pip install pymongo
- verification de l'installation dans le terminal :
  pip show pymongo

## pandas

- On a besoin d'installer la bibliotheque pandas
- Commande pour l'installation:
  pip install pandas
- verification de l'installation dans le terminal :
  pip show pandas

## apscheduler

- On a besoin d'installer la bibliotheque apscheduler
- Commande pour l'installation:
  pip install apscheduler
- verification de l'installation dans le terminal :
  pip show apscheduler

# Execution du projet

- Pour executer le projet il faut :
  - lancer MySQL et MongoDB
  - Ouvrir la racine du projet et tapper la commande :
    cd ELT-tool
    cd 01_SW
    streamlit run Accueil.py
