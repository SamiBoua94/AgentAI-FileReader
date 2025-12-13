# URL du Dashboard Looker Studio (À remplacer par votre lien)
DASHBOARD_URL = "https://lookerstudio.google.com/s/n-s_GBiwibs"

# --- Menu Principal (Tkinter) ---
def main_menu():
    """Affiche le menu principal de l'application avec un design moderne."""
    import tkinter as tk
    from tkinter import ttk
    import webbrowser
    import agent_vision
    import sys
    
    # Couleurs du thème (Dracula / Modern Dark)
    BG_COLOR = "#1E1E2E"       # Fond principal (Deep Blue/Black)
    CARD_COLOR = "#2D2D44"     # Fond des conteneurs
    TEXT_COLOR = "#E0E0E0"     # Texte principal
    ACCENT_COLOR = "#4CAF50"   # Vert (Action principale)
    HOVER_COLOR = "#3E3E5E"    # Couleur au survol générique
    
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Agent Vision - Accueil")
    root.geometry("600x600")
    root.configure(bg=BG_COLOR)
    
    # Centrer la fenêtre
    # (Optionnel, parfois buggé sur certains multi-écrans, on garde geometry simple)

    # --- Fonctions Utilitaires ---
    def on_enter(e, btn, hover_col):
        btn['bg'] = hover_col

    def on_leave(e, btn, original_col):
        btn['bg'] = original_col

    # --- Interface ---
    
    # Conteneur Centré (Card effect)
    main_container = tk.Frame(root, bg=BG_COLOR)
    main_container.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
    
    # Header Logo/Titre
    header_frame = tk.Frame(main_container, bg=BG_COLOR)
    header_frame.pack(fill=tk.X, pady=(0, 30))
    
    title_label = tk.Label(
        header_frame,
        text="🤖 AGENT VISION",
        font=("Segoe UI", 28, "bold"),
        fg="#00E676", # Vert néon plus moderne
        bg=BG_COLOR
    )
    title_label.pack()
    
    subtitle_label = tk.Label(
        header_frame,
        text="Votre Assistant Intelligent d'Analyse",
        font=("Segoe UI", 11),
        fg="#A0A0C0",
        bg=BG_COLOR
    )
    subtitle_label.pack(pady=(5, 0))

    # Zone de Boutons (Dans un cadre plus clair "Card")
    # Pour un design épuré, on garde le fond uni mais on espace bien les boutons
    btn_frame = tk.Frame(main_container, bg=BG_COLOR)
    btn_frame.pack(fill=tk.BOTH, expand=True)

    def create_modern_btn(parent, text, command, base_col, hover_col, icon=""):
        # Frame pour le padding externe
        frame = tk.Frame(parent, bg=BG_COLOR, pady=8)
        frame.pack(fill=tk.X)
        
        # Le bouton lui-même
        btn = tk.Button(
            frame,
            text=f"{icon}   {text}",
            font=("Segoe UI", 12, "bold"),
            bg=base_col,
            fg="white",
            activebackground=hover_col,
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=15,
            cursor="hand2",
            command=command,
            anchor="center" # Centrer le texte
        )
        btn.pack(fill=tk.X, ipady=5) # ipady pour donner du volume
        
        # Effets Hover
        btn.bind("<Enter>", lambda e: on_enter(e, btn, hover_col))
        btn.bind("<Leave>", lambda e: on_leave(e, btn, base_col))
        
        return btn

    # 1. Ajouter une image (Action Principale -> Plus visible)
    create_modern_btn(
        btn_frame, 
        "NOUVELLE ANALYSE", 
        agent_vision.start_analysis, 
        "#6C5CE7", # Violet moderne
        "#8E7CFF",
        icon="📸"
    )
    
    # Séparateur visuel
    tk.Frame(btn_frame, bg=BG_COLOR, height=10).pack()

    # 2. Base de données
    create_modern_btn(
        btn_frame, 
        "Base de Données (Sheets)", 
        open_db_action, 
        "#2D2D44", # Sombre (Secondaire)
        "#3D3D5C",
        icon="📊"
    )
    
    # 3. Dashboard
    create_modern_btn(
        btn_frame, 
        "Tableau de Bord (Looker)", 
        open_dashboard_action, 
        "#2D2D44", # Sombre (Secondaire)
        "#3D3D5C",
        icon="📈"
    )

    # Spacer
    tk.Frame(btn_frame, bg=BG_COLOR, height=20).pack()
    
    # 4. Quitter
    btn_exit = tk.Button(
        btn_frame,
        text="Quitter l'application",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg="#FF5252",
        activebackground=BG_COLOR,
        activeforeground="#FF8A80",
        relief=tk.FLAT,
        bd=0,
        cursor="hand2",
        command=close_app_action
    )
    btn_exit.pack(pady=10)

    # Footer
    footer_label = tk.Label(
        root,
        text="v2.0 • Agent Vision",
        font=("Segoe UI", 8),
        fg="#54546E",
        bg=BG_COLOR
    )
    footer_label.pack(side=tk.BOTTOM, pady=15)
    
    root.mainloop()

# --- Wrappers pour les commandes (Scope) ---
def open_db_action():
    import webbrowser
    import agent_vision
    webbrowser.open(agent_vision.
    )

def open_dashboard_action():
    import webbrowser
    webbrowser.open(DASHBOARD_URL)

def close_app_action():
    import sys
    sys.exit()

if __name__ == "__main__":
    main_menu()
