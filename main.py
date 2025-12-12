import tkinter as tk
from tkinter import ttk
import webbrowser
import agent_vision
import sys

def main_menu():
    """Affiche le menu principal de l'application."""
    
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Agent Vision - Accueil")
    root.geometry("500x450")
    root.configure(bg="#2b2b2b")
    
    # Style
    style = ttk.Style()
    style.theme_use('clam')
    
    # --- UI Elements ---
    
    # Header
    header_frame = tk.Frame(root, bg="#2b2b2b", pady=30)
    header_frame.pack(fill=tk.X)
    
    title_label = tk.Label(
        header_frame,
        text="🤖 AGENT VISION",
        font=("Segoe UI", 24, "bold"),
        fg="#4CAF50",
        bg="#2b2b2b"
    )
    title_label.pack()
    
    subtitle_label = tk.Label(
        header_frame,
        text="Bienvenue dans votre assistant d'analyse",
        font=("Segoe UI", 12),
        fg="#B0BEC5",
        bg="#2b2b2b"
    )
    subtitle_label.pack(pady=(5, 0))
    
    # Buttons Frame
    btn_frame = tk.Frame(root, bg="#2b2b2b", padx=50)
    btn_frame.pack(fill=tk.BOTH, expand=True)
    
    # Helper for creating buttons
    def create_btn(text, command, color="#42A5F5"):
        btn = tk.Button(
            btn_frame,
            text=text,
            font=("Segoe UI", 12),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=command
        )
        return btn

    # 1. Ajouter une image -> Lance l'analyse
    btn_add = create_btn("📸  Ajouter une image", agent_vision.start_analysis, color="#4CAF50")
    btn_add.pack(fill=tk.X, pady=10)
    
    # 2. Consulter la base de données -> Ouvre le Google Sheet
    def open_db():
        webbrowser.open(agent_vision.SHEET_URL)
    
    btn_db = create_btn("📊  Consulter la base de données", open_db, color="#2196F3")
    btn_db.pack(fill=tk.X, pady=10)
    
    # 3. Accéder au tableau de bord -> Vide pour le moment
    def open_dashboard():
        pass 
    
    btn_dash = create_btn("📈  Accéder au tableau de bord", open_dashboard, color="#9C27B0")
    btn_dash.pack(fill=tk.X, pady=10)
    
    # 4. Fermer -> Ferme tout
    def close_app():
        root.destroy()
        sys.exit()

    btn_exit = create_btn("❌  Fermer", close_app, color="#D32F2F")
    btn_exit.pack(fill=tk.X, pady=10)
    
    # Footer
    footer_label = tk.Label(
        root,
        text="© 2025 Agent Vision - v1.0",
        font=("Segoe UI", 8),
        fg="#546E7A",
        bg="#2b2b2b"
    )
    footer_label.pack(side=tk.BOTTOM, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main_menu()
