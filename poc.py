import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")

# client = OpenAI()

# # 1) Vytvořit asistenta - dostane instrukce "jsi expert na..., odpovídej pouze na základě informací ze souboru"

# assistant = client.beta.assistants.create(
#     name="Expert na PDF",
#     instructions="Jsi expert na dokumenty. Odpovídej pouze na základě informací, které najdeš v poskytnutých souborech. Pokud odpověď v souborech není, řekni, že to nevíš.",
#     model="gpt-4o-mini",
#     tools=[{"type": "file_search"}],
# )

# 2) Nahrání souboru a vytvoření vector store
