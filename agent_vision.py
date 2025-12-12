import os
import json
import asyncio
from typing import List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 1. Configuration
load_dotenv()

# --- Modèle de Données (Ce qu'on veut extraire de la photo) ---
class AnalyseResult(BaseModel):
    summary: str = Field(description="Un résumé court du contenu de l'image")
    key_data: dict = Field(description="Les données chiffrées ou importantes (ex: montant, dates)")
    action_items: List[str] = Field(description="Liste des actions à entreprendre basées sur l'image")
    urgency: str = Field(description="Niveau d'urgence : Low, Medium, High")

# --- Fonctions Simulées (Vos Outils) ---
async def update_dashboard(data: dict):
    """Simule l'envoi des données vers un Notion/Excel/Dashboard."""
    print(f"\n[DASHBOARD] Mise à jour en cours...")
    await asyncio.sleep(1) # Simulation délai réseau
    print(f"[DASHBOARD] ✅ Données enregistrées : {json.dumps(data, indent=2)}")

async def schedule_reminder(actions: List[str]):
    """Simule la programmation de rappels."""
    print(f"\n[RAPPEL] Analyse des rappels à créer...")
    for action in actions:
        # Ici on pourrait appeler l'API de Google Calendar ou Slack
        print(f"[RAPPEL] ⏰ Rappel programmé pour : '{action}'")

# --- Fonctions Utilitaires ---
def encode_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# --- Cœur de l'Agent ---
async def process_image(image_path: str):
    print(f"--- Analyse de l'image : {image_path} ---")
    
    # 2. Préparation du Modèle Vision
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest") 
    
    parser = JsonOutputParser(pydantic_object=AnalyseResult)
    
    # 2b. Encodage de l'image en Base64
    try:
        base64_image = encode_image(image_path)
    except Exception as e:
        print(f"Erreur de lecture de l'image : {e}")
        return

    # 3. Construction de la requête avec l'image (Format Data URI)
    message = HumanMessage(
        content=[
            {
                "type": "text", 
                "text": "Analyse cette image. Extrais les informations pour mettre à jour mon dashboard de suivi. \n" + parser.get_format_instructions()
            },
            {
                "type": "image_url", 
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            }
        ]
    )

    try:
        print("Envoi de la requête à Gemini...")
        # 4. Appel AI
        response = await llm.ainvoke([message])
        
        # 5. Parsing du résultat
        parsed_result = parser.parse(response.content)
        
        # 6. Exécution des actions en Parallèle
        await asyncio.gather(
            update_dashboard(parsed_result['key_data']),
            schedule_reminder(parsed_result['action_items'])
        )
        
        print("\n--- Terminé avec succès ---")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Erreur lors de l'exécution : {e}")

# --- Sélection de Photo ---
def select_photo():
    """Ouvre une boîte de dialogue pour sélectionner une photo."""
    import tkinter as tk
    from tkinter import filedialog, messagebox
    
    # Créer la fenêtre principale (cachée)
    root = tk.Tk()
    root.withdraw()
    
    # Message de bienvenue
    messagebox.showinfo(
        "Agent Vision",
        "Bienvenue dans l'Agent Vision!\n\n"
        "Cliquez sur OK pour sélectionner une photo à analyser."
    )
    
    # Définir les types de fichiers acceptés
    filetypes = [
        ("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
        ("JPEG", "*.jpg *.jpeg"),
        ("PNG", "*.png"),
        ("Tous les fichiers", "*.*")
    ]
    
    # Ouvrir le dialogue de sélection
    filepath = filedialog.askopenfilename(
        title="Sélectionnez une photo à analyser",
        filetypes=filetypes,
        initialdir=os.getcwd()
    )
    
    root.destroy()
    return filepath

def save_to_picturetaken(source_path: str) -> str:
    """Copie la photo dans le dossier picturetaken et retourne le nouveau chemin."""
    import shutil
    from datetime import datetime
    
    # Créer le dossier picturetaken s'il n'existe pas
    picturetaken_folder = os.path.join(os.getcwd(), "picturetaken")
    if not os.path.exists(picturetaken_folder):
        os.makedirs(picturetaken_folder)
        print(f"📁 Dossier créé : {picturetaken_folder}")
    
    # Générer un nom de fichier unique avec timestamp
    filename = os.path.basename(source_path)
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{name}_{timestamp}{ext}"
    
    # Copier le fichier
    destination = os.path.join(picturetaken_folder, new_filename)
    shutil.copy2(source_path, destination)
    print(f"💾 Photo copiée dans : {destination}")
    
    return destination

# --- Lancement ---
if __name__ == "__main__":
    # Sélection interactive de la photo
    image_path = select_photo()
    
    if image_path:
        if os.path.exists(image_path):
            print(f"📷 Photo sélectionnée : {image_path}")
            
            # Copier la photo dans le dossier picturetaken
            saved_path = save_to_picturetaken(image_path)
            
            # Analyser la photo
            asyncio.run(process_image(saved_path))
        else:
            print(f"⚠️  Image introuvable : {image_path}")
    else:
        print("❌ Aucune photo sélectionnée.")
