import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# 1. Configuration
load_dotenv()

# Configure l'API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("⚠️  Erreur: GOOGLE_API_KEY non trouvée dans le fichier .env")
    exit(1)

genai.configure(api_key=api_key)

# Fichier pour stocker le compteur de demandes
COUNTER_FILE = os.path.join(os.path.dirname(__file__), "request_counter.json")

# --- Gestion du Compteur de Demandes ---
def get_next_request_id() -> int:
    """Récupère et incrémente le compteur de demandes."""
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            data = json.load(f)
            current_id = data.get("last_id", 0)
    else:
        current_id = 0
    
    new_id = current_id + 1
    
    with open(COUNTER_FILE, "w") as f:
        json.dump({"last_id": new_id}, f)
    
    return new_id

# URL du Google Sheet où les logs seront enregistrés
# URL du Google Sheet où les logs seront enregistrés
SHEET_URL = "https://docs.google.com/spreadsheets/d/1uEE2YIpzs74-JCcEb5NvQCeUm9VgV_owTRocvl34qH4/edit?usp=sharing"

# --- Google Sheets Integration ---
def log_to_google_sheet(request_id, date, image_name, title, description):
    """Enregistre les données dans Google Sheets.
    Utilise l'URL du sheet fourni pour ouvrir le document.
    """
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_file = os.path.join(os.path.dirname(__file__), 'credentials.json')
    
    if not os.path.exists(creds_file):
        print("⚠️  Erreur: credentials.json introuvable. Logging désactivé.")
        return

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        
        # Ouvrir le sheet par URL
        sheet = client.open_by_url(SHEET_URL).sheet1
        
        row = [request_id, date, image_name, title, description]
        sheet.append_row(row)
        print("✅ Données enregistrées dans Google Sheet !")
        
    except Exception as e:
        print(f"❌ Erreur Google Sheets : {e}")

# --- Affichage des Résultats (Tkinter) ---
def show_results_window(request_id, image_name, date_time, titre, description):
    """Affiche les résultats de l'analyse dans une fenêtre Tkinter."""
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title(f"Agent Vision - Résultat #{request_id}")
    root.geometry("600x500")
    root.configure(bg="#2b2b2b")
    
    # Style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Frame principal
    main_frame = tk.Frame(root, bg="#2b2b2b", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Titre de la fenêtre
    title_label = tk.Label(
        main_frame, 
        text="🤖 AGENT VISION - Résultat de l'analyse",
        font=("Segoe UI", 16, "bold"),
        fg="#4CAF50",
        bg="#2b2b2b"
    )
    title_label.pack(pady=(0, 20))
    
    # Frame pour les informations
    info_frame = tk.Frame(main_frame, bg="#3c3c3c", padx=15, pady=15)
    info_frame.pack(fill=tk.X, pady=(0, 15))
    
    # Informations
    info_labels = [
        (f"📋 Demande numéro : {request_id}", "#FFA726"),
        (f"🖼️ Nom de l'image : {image_name}", "#42A5F5"),
        (f"📅 Date : {date_time}", "#AB47BC"),
        (f"📌 Titre : {titre}", "#66BB6A")
    ]
    
    for text, color in info_labels:
        label = tk.Label(
            info_frame,
            text=text,
            font=("Segoe UI", 11),
            fg=color,
            bg="#3c3c3c",
            anchor="w"
        )
        label.pack(fill=tk.X, pady=3)
    
    # Label pour la description
    desc_label = tk.Label(
        main_frame,
        text="📝 Description du contenu :",
        font=("Segoe UI", 12, "bold"),
        fg="#FFFFFF",
        bg="#2b2b2b",
        anchor="w"
    )
    desc_label.pack(fill=tk.X, pady=(10, 5))
    
    # Zone de texte scrollable pour la description
    desc_text = scrolledtext.ScrolledText(
        main_frame,
        wrap=tk.WORD,
        font=("Segoe UI", 10),
        bg="#3c3c3c",
        fg="#FFFFFF",
        height=10,
        padx=10,
        pady=10
    )
    desc_text.pack(fill=tk.BOTH, expand=True)
    desc_text.insert(tk.END, description)
    desc_text.config(state=tk.DISABLED)
    
    # Bouton Fermer
    close_btn = tk.Button(
        main_frame,
        text="Fermer",
        font=("Segoe UI", 11),
        bg="#4CAF50",
        fg="white",
        padx=30,
        pady=8,
        command=root.destroy
    )
    close_btn.pack(pady=(15, 0))
    
    # Afficher la fenêtre
    root.mainloop()

# --- Cœur de l'Agent ---
def process_image(image_path: str):
    # Récupérer l'ID de la demande
    request_id = get_next_request_id()
    
    # Récupérer la date et l'heure actuelles
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Récupérer le nom de l'image
    image_name = os.path.basename(image_path)
    
    print(f"\n🔄 Traitement en cours...")
    
    titre = "null"
    description = "null"
    
    try:
        # Charger l'image
        img = Image.open(image_path)
        
        # Utiliser le modèle Gemini Flash
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Créer le prompt
        prompt = """Analyse cette image et fournis:
1. Un titre court décrivant le sujet principal
2. Une description détaillée de ce que tu vois

Réponds au format JSON suivant:
{
    "titre": "titre court ici",
    "description": "description détaillée ici"
}"""
        
        # Générer la réponse
        response = model.generate_content([prompt, img])
        
        # Parser la réponse JSON
        response_text = response.text.strip()
        
        # Nettoyer la réponse si elle contient des balises markdown
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()
        
        result = json.loads(response_text)
        
        # Mettre à jour avec les résultats
        titre = result.get('titre', "null")
        description = result.get('description', "null")
        
        # Afficher les résultats dans une fenêtre Tkinter
        show_results_window(request_id, image_name, current_datetime, titre, description)
        
    except json.JSONDecodeError as e:
        print(f"\n⚠️  Erreur de parsing JSON. Réponse brute:")
        print(response.text)
        print(f"\nErreur: {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ Erreur lors de l'exécution : {e}")
        
    finally:
        # Toujours enregistrer dans Google Sheets, même en cas d'erreur (avec valeurs "null" si échec)
        log_to_google_sheet(request_id, current_datetime, image_name, titre, description)

# --- Sélection de Photo (Tkinter) ---
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

# --- Analyse (Fonction principale) ---
def start_analysis():
    """Lance le processus de sélection et d'analyse."""
    print("\n" + "="*60)
    print("  🤖 AGENT VISION - Analyse d'images avec Gemini")
    print("="*60)
    
    # Sélection de la photo via tkinter
    image_path = select_photo()
    
    if image_path:
        if os.path.exists(image_path):
            print(f"\n📷 Photo sélectionnée : {image_path}")
            
            # Copier la photo dans le dossier picturetaken
            saved_path = save_to_picturetaken(image_path)
            
            # Analyser la photo
            process_image(saved_path)
        else:
            print(f"\n⚠️  Image introuvable : {image_path}")
            print("Vérifiez que le fichier existe et que le chemin est correct.")
    else:
        print("\n❌ Aucune photo sélectionnée.")

# --- Lancement ---
if __name__ == "__main__":
    start_analysis()
