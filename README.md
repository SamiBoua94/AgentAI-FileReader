# Agent AI - Instructions

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
    `c:\Users\HP\.gemini\antigravity\playground\scalar-aurora\AgentAntigravity\`

## 2. Préparation du Google Sheet

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

## 3. Installation des librairies

Nous devons installer :
```bash
pip install gspread oauth2client
```



