
# 🤖 Agent AI Vision - Assistant d'Analyse Intelligent

**Agent Vision** est une application Python exploitant la puissance de l'Intelligence Artificielle (**Modele : Gemini flash 1.5**) pour analyser, classer et extraire des informations à partir d'images et de documents.

---

## 📑 Sommaire
1. [Objectif et Cas d'Usage](#1-objectif-et-cas-dusage)
2. [Aperçu de l'Interface](#2-aperçu-de-linterface)
3. [Technologies Utilisées](#3-technologies-utilisées)
4. [Tutoriels et Installation](#4-tutoriels-et-installation)

---

## 1. Objectif et Cas d'Usage

Cette application a été conçue pour résoudre des problèmes concrets de gestion de flux visuels et textuels dans des environnements sous tension.

### a. 🏛️ Administration & Service Public
**Le Problème :** Les fonctionnaires font face à un volume massif de courriers et de formulaires papier. Le tri manuel est chronophage, et retrouver l'état d'avancement d'un dossier pour répondre à un citoyen est souvent complexe.

**La Solution Agent Vision :**
*   **Numérisation & Analyse** : L'IA lit le courrier, identifie le type de demande et le résume automatiquement.
*   **Centralisation** : Les données sont envoyées dans une base de données collaborative.
*   **Transparence** : Un tableau de bord permet de suivre en temps réel l'état des demandes pour informer les citoyens instantanément.

### b. 🏥 Santé & Accès aux Soins
**Le Problème :** L'accès à la médecine en France est tendu (déserts médicaux, urgences saturées). Les médecins manquent de temps pour trier les patients par gravité avant la consultation.

**La Solution Agent Vision :**
*   **Pré-diagnostic** : Les patients peuvent envoyer une photo (ex: problème dermatologique, blessure).
*   **Priorisation** : L'IA analyse l'image pour suggérer un niveau d'urgence et propose un pre-diagnostic.
*   **Gestion** : Cela aide les régulateurs et médecins à prioriser les rendez-vous et optimiser le parcours de soin.

---

## 2. Aperçu de l'Interface


**Page d'accueil**

<img width="449" height="468" alt="Image" src="https://github.com/user-attachments/assets/b3cbe10d-ecd8-4e1f-ae04-1ed923beae6c" />

**Tableau de bord**

<img width="944" height="395" alt="TablBord" src="https://github.com/user-attachments/assets/0923ccd6-7496-4e49-87ab-6584133aa442" />


## 3. Technologies Utilisées


Ce projet repose sur une stack moderne et légère :

*   **Langage** : [Python 3.x](https://www.python.org/) 🐍
*   **Intelligence Artificielle** :Google AI studio [Google Gemini Pro Vision](https://deepmind.google/technologies/gemini/) (via `google-generativeai`) 🧠
*   **Interface Graphique (GUI)** : Tkinter (Native Python) 🖥️
*   **Base de Données** : Google Sheets (via `gspread` & API Google Drive) 📊
*   **Dashboard** : Google Looker Studio (Business Intelligence) 📈

---

## 4. Tutoriels et Installation

Des guides détaillés sont disponibles dans ce dépôt pour vous aider à configurer le projet :

## A. Préparation du Google Sheet

1.  Créez un nouveau Google Sheet dans votre navigateur.
2.  Donnez-lui un nom (ex: `Suivi Agent Vision`).
3.  Ouvrez le fichier `credentials.json` avec un éditeur de texte et copiez l'adresse email qui ressemble à :
    `client_email": "sheets-bot@votre-projet.iam.gserviceaccount.com"`
4.  Retournez sur votre Google Sheet, cliquez sur **"Partager"** (en haut à droite) et **collez cette adresse email** en lui donnant les droits d'**Éditeur**.
5.  Dans la première ligne du Sheet, mettez les en-têtes suivants :
    *   Colonne A : **ID**
    *   Colonne B : **Date**
    *   Colonne C : **Nom Image**
    *   Colonne D : **Titre**
    *   Colonne E : **Description**

## B. Installation des librairies

Nous devons installer :
```bash
pip install gspread oauth2client
```

### Installation Rapide

1.  **Cloner le dépôt :**
    ```bash
    mkdir AgentAI-FileReader
    cd AgentAI-FileReader
    git clone https://github.com/SamiBoua94/AgentAI-FileReader.git
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurer les clés API :**
    *   Créez un fichier `.env` avec votre `GOOGLE_API_KEY`.
    *   Ajoutez votre fichier `credentials.json` (Google Cloud) à la racine.

4.  **Lancer l'application :**
    ```bash
    py main.py
    ```

---

Vous avez besoin d'un compte google cloud platform.

Voici comment lancer votre agent :
Votre environnement n'a pas Pytnon installé (ou configuré dans le PATH). 



## 1. Installer Python
1. Téléchargez Python sur [python.org/downloads](https://www.python.org/downloads/).
2. **IMPORTANT** : Cochez la case **"Add Python to PATH"** lors de l'installation.
3. Redémarrez votre terminal (ou l'ordinateur).

## 2. Configurer la Clé API
1. Ouvrez le fichier `.env` dans ce dossier.
2. Remplacez `votre_cle_google_ici...` par votre vraie clé (disponible sur [Google AI Studio](https://aistudio.google.com/app/apikey)).

## 3. Installer les dépendances
Ouvrez un terminal dans ce dossier et lancez :
```bash
pip install -U langchain-google-genai pillow pydantic python-dotenv
```

## 4. Lancer l'Agent
```bash
python main.py
```
Puis suivez les instructions.


# Guide d'Intégration de la base de données Google Cloud

Pour enregistrer vos données dans un Google Sheet, nous devons autoriser un "robot" (Service Account) à écrire dans votre fichier.

## 1. Création du Projet et Clé (Console Google Cloud)

1.  Allez sur la [Console Google Cloud](https://console.cloud.google.com/).
2.  Créez un nouveau projet (ou utilisez l'existant).
3.  Cherchez et activez ces deux APIs :
    *   **Google Sheets API**
    *   **Google Drive API**
4.  Allez dans **"IAM et administration"** > **"Comptes de service"**.
5.  Cliquez sur **"Créer un compte de service"**. Donnez-lui un nom (ex: `sheets-bot`).
6.  Une fois créé, cliquez sur les trois petits points à droite > **"Gérer les clés"**.
7.  Cliquez sur **"Ajouter une clé"** > **"Créer une clé"** > **JSON**.
8.  Le fichier va se télécharger. **Renommez-le** en `credentials.json` et **placez-le** dans votre dossier de projet :


## 3. Installation des librairies

Nous devons installer :
```bash
pip install gspread oauth2client
```



