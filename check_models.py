import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Pas de clé API trouvée !")
else:
    genai.configure(api_key=api_key)
    try:
        print("--- Modèles Disponibles ---")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Nom: {m.name}")
                print(f"  Méthodes: {m.supported_generation_methods}")
                print()
    except Exception as e:
        print(f"Erreur lors du listing : {e}")
