import os
import sys
from google import genai

# read API key explicitly from environment and fail proprement si manquante
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    sys.stderr.write(
        "Erreur : la variable d'environnement GEMINI_API_KEY n'est pas définie.\n"
        "Définissez-la temporairement : export GEMINI_API_KEY=\"VOTRE_CLE\"\n"
        "Ou créez un fichier .env à la racine contenant : GEMINI_API_KEY=VOTRE_CLE\n"
    )
    sys.exit(1)

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Who's the actual french prime minister? Check on the web if needed."
)
print(response.text)
