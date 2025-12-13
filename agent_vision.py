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
        
        # Structure : ID | Progression | Date | Image | Titre | Description
        # On met 0 par défaut dans Progression
        row = [request_id, 0, date, image_name, title, description]
        sheet.append_row(row)
        print("✅ Données enregistrées dans Google Sheet !")
        
    except Exception as e:
        print(f"❌ Erreur Google Sheets : {e}")

# --- Affichage des Résultats (Tkinter) ---
# --- Affichage des Résultats (Tkinter) ---
def show_results_window(request_id, image_name, date_time, titre, description):
    """Affiche les résultats de l'analyse dans une fenêtre Tkinter moderne."""
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    
    # Couleurs du thème (Dracula / Modern Dark)
    BG_COLOR = "#1E1E2E"       # Fond principal
    CARD_COLOR = "#2D2D44"     # Fond des conteneurs
    TEXT_COLOR = "#E0E0E0"     # Texte principal
    ACCENT_COLOR = "#4CAF50"   # Vert (Action principale)
    HOVER_COLOR = "#3E3E5E"    # Couleur au survol
    
    
    # Déterminer si on utilise une fenêtre Toplevel (si une racine existe déjà) ou Tk
    if tk._default_root:
        root = tk.Toplevel()
        # Bring to front
        root.lift()
        root.attributes('-topmost',True)
        root.after_idle(root.attributes,'-topmost',False)
    else:
        root = tk.Tk()
        
    root.title(f"Agent Vision - Résultat #{request_id}")
    root.geometry("700x650") 
    root.configure(bg=BG_COLOR)
    
    # Centrage implicite via geometry souvent géré par l'OS
    
    # Frame principal avec padding pour "respirer"
    main_frame = tk.Frame(root, bg=BG_COLOR, padx=30, pady=30)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Header
    title_label = tk.Label(
        main_frame, 
        text="RÉSULTAT DE L'ANALYSE",
        font=("Segoe UI", 20, "bold"),
        fg="#00E676", # Vert moderne
        bg=BG_COLOR
    )
    title_label.pack(anchor="w", pady=(0, 20))
    
    # --- Card Informations (ID, Date, Image, Titre) ---
    info_card = tk.Frame(main_frame, bg=CARD_COLOR, padx=20, pady=20)
    info_card.pack(fill=tk.X, pady=(0, 20))
    
    # Helper pour lignes d'info
    def create_info_row(parent, label_text, value_text, value_color="#E0E0E0"):
        row = tk.Frame(parent, bg=CARD_COLOR)
        row.pack(fill=tk.X, pady=4)
        
        lbl = tk.Label(
            row, text=label_text, font=("Segoe UI", 10, "bold"), 
            fg="#A0A0C0", bg=CARD_COLOR, width=15, anchor="w"
        )
        lbl.pack(side=tk.LEFT)
        
        val = tk.Label(
            row, text=value_text, font=("Segoe UI", 11), 
            fg=value_color, bg=CARD_COLOR, anchor="w"
        )
        val.pack(side=tk.LEFT, fill=tk.X, expand=True)

    create_info_row(info_card, "DEMANDE #", str(request_id), "#FFA726") # Orange
    create_info_row(info_card, "IMAGE", image_name, "#42A5F5")  # Bleu
    create_info_row(info_card, "DATE", date_time, "#AB47BC")    # Violet
    tk.Frame(info_card, bg="#3E3E5E", height=1).pack(fill=tk.X, pady=10) # Séparateur
    create_info_row(info_card, "TITRE", titre, "#66BB6A")       # Vert clair

    # --- Section Description ---
    desc_label = tk.Label(
        main_frame,
        text="Description Détaillée",
        font=("Segoe UI", 12, "bold"),
        fg="#FFFFFF",
        bg=BG_COLOR,
        anchor="w"
    )
    desc_label.pack(fill=tk.X, pady=(0, 10))
    
    desc_text = scrolledtext.ScrolledText(
        main_frame,
        wrap=tk.WORD,
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        height=10,
        padx=15,
        pady=15,
        relief=tk.FLAT,
        insertbackground="white" # Curseur blanc
    )
    desc_text.pack(fill=tk.BOTH, expand=True)
    desc_text.insert(tk.END, description)
    desc_text.config(state=tk.DISABLED)
    
    # --- Boutons ---
    btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
    btn_frame.pack(fill=tk.X, pady=(25, 0))

    def on_enter(e, btn, col):
        btn['bg'] = col
    def on_leave(e, btn, col):
        btn['bg'] = col

    # Bouton Retour
    back_btn = tk.Button(
        btn_frame,
        text="⬅️ Retour au Menu",
        font=("Segoe UI", 11, "bold"),
        bg="#2D2D44", # Sombre
        fg="white",
        activebackground="#3D3D5C",
        activeforeground="white",
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=12,
        cursor="hand2",
        command=root.destroy
    )
    back_btn.pack(side=tk.LEFT)
    back_btn.bind("<Enter>", lambda e: on_enter(e, back_btn, "#3D3D5C"))
    back_btn.bind("<Leave>", lambda e: on_leave(e, back_btn, "#2D2D44"))

    # Bouton Fermer (Quitte l'application)
    def quit_app():
        import sys
        root.destroy()
        sys.exit()

    close_btn = tk.Button(
        btn_frame,
        text="Quitter ❌",
        font=("Segoe UI", 11, "bold"),
        bg="#FF5252", # Rouge
        fg="white",
        activebackground="#FF8A80",
        activeforeground="white",
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=12,
        cursor="hand2",
        command=quit_app
    )
    close_btn.pack(side=tk.RIGHT)
    close_btn.bind("<Enter>", lambda e: on_enter(e, close_btn, "#FF1744"))
    close_btn.bind("<Leave>", lambda e: on_leave(e, close_btn, "#FF5252"))
    
    # Afficher la fenêtre
    if isinstance(root, tk.Tk):
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
        # Vérifier si c'est une erreur de quota (429 Resource Exhausted)
        error_str = str(e)
        if "429" in error_str or "ResourceExhausted" in error_str or "quota" in error_str.lower():
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw() # Cacher la fenêtre principale
            messagebox.showerror(
                "Erreur de Quota API",
                "🚫 L'analyse a échoué.\n\n"
                "Raison : La limite des requêtes API Gemini journalière a été atteinte.\n"
                "Veuillez réessayer plus tard (souvent quelques minutes suffisent pour la limite par minute, ou demain pour la limite journalière)."
            )
            root.destroy()
            print("\n❌ Erreur QUOTA API atteinte.")
        else:
            traceback.print_exc()
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'analyse :\n{e}")
            root.destroy()
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
