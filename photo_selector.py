"""
Photo Selector - Interface graphique pour sélectionner une photo à analyser
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from agent_vision import process_image
import asyncio


def select_photo():
    """Ouvre une boîte de dialogue pour sélectionner une photo."""
    # Définir les types de fichiers acceptés
    filetypes = [
        ("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
        ("JPEG", "*.jpg *.jpeg"),
        ("PNG", "*.png"),
        ("Tous les fichiers", "*.*")
    ]
    
    # Ouvrir le dialogue de sélection de fichier
    filepath = filedialog.askopenfilename(
        title="Sélectionnez une photo à analyser",
        filetypes=filetypes,
        initialdir=os.getcwd()
    )
    
    return filepath


def main():
    """Point d'entrée principal de l'application."""
    # Créer la fenêtre principale (cachée)
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    
    # Afficher un message de bienvenue
    messagebox.showinfo(
        "Agent Vision - Photo Selector",
        "Bienvenue dans l'Agent Vision!\n\n"
        "Cliquez sur OK pour sélectionner une photo à analyser."
    )
    
    # Sélectionner la photo
    photo_path = select_photo()
    
    if photo_path:
        # Vérifier que le fichier existe
        if os.path.exists(photo_path):
            print(f"📷 Photo sélectionnée : {photo_path}")
            
            # Confirmer l'analyse
            confirm = messagebox.askyesno(
                "Confirmer l'analyse",
                f"Voulez-vous analyser cette image ?\n\n{os.path.basename(photo_path)}"
            )
            
            if confirm:
                print("🔄 Lancement de l'analyse...")
                # Lancer l'analyse de l'image
                asyncio.run(process_image(photo_path))
                
                messagebox.showinfo(
                    "Analyse terminée",
                    "L'analyse de la photo est terminée!\n\n"
                    "Consultez la console pour voir les résultats."
                )
            else:
                print("❌ Analyse annulée par l'utilisateur.")
        else:
            messagebox.showerror(
                "Erreur",
                f"Le fichier sélectionné n'existe pas :\n{photo_path}"
            )
    else:
        print("❌ Aucune photo sélectionnée.")
        messagebox.showwarning(
            "Aucune sélection",
            "Aucune photo n'a été sélectionnée.\n\n"
            "L'application va se fermer."
        )
    
    # Fermer proprement
    root.destroy()


if __name__ == "__main__":
    main()
