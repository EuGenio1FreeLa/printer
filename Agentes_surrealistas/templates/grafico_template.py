import sys
import numpy as np
from dotenv import load_dotenv
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

db_path = "{{DB_FOLDER_NAME}}"
db = FAISS.load_local(db_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

faiss_index = db.index
documentos = list(db.docstore._dict.values())

textos = [doc.page_content[:80].replace("\n", " ") for doc in documentos]
vetores = np.array([faiss_index.reconstruct(i) for i in range(len(documentos))])

perplexidade = min(30, len(textos) - 1) if len(textos) > 2 else 1

tsne = TSNE(n_components=2, perplexity=perplexidade, random_state=42)
vetores_2d = tsne.fit_transform(vetores)

plt.figure(figsize=(14, 9))
for i, texto in enumerate(textos):
    x, y = vetores_2d[i]
    plt.scatter(x, y, marker='o')
    plt.text(x + 0.5, y + 0.5, f"{texto[:40]}...", fontsize=7)

plt.title("Visualizacao dos Embeddings - {{PROJECT_NAME}}")
plt.grid(True)
plt.tight_layout()
plt.savefig("embeddings_visualizacao.png")
print("Grafico salvo em embeddings_visualizacao.png")
