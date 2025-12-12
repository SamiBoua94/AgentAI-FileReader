# Agent Antigravity - Instructions

Votre environnement n'a pas Pytnon installé (ou configuré dans le PATH). Voici comment lancer votre agent :

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
Déposez une image `exemple.jpg` à côté du script, puis lancez :
```bash
python agent_vision.py
```
