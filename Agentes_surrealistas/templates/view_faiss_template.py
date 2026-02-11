import json
import sys
import numpy as np
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

db_path = "{{DB_FOLDER_NAME}}"
db = FAISS.load_local(db_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

faiss_index = db.index
documentos = list(db.docstore._dict.values())

dados = []

for i, doc in enumerate(documentos):
    vetor = faiss_index.reconstruct(i)
    item = {
        "id": i,
        "conteudo": doc.page_content.replace("\n", " ").strip(),
        "vetor_parcial": vetor[:10].tolist()
    }
    dados.append(item)

with open("faiss_exportado.json", "w", encoding="utf-8") as jsonfile:
    json.dump(dados, jsonfile, ensure_ascii=False, indent=2)

print(f"Arquivo faiss_exportado.json criado com {len(dados)} documentos.")
