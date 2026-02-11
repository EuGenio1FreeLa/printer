import os
import sys
import warnings

sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate

load_dotenv()

# --- Configuracao do projeto: {{PROJECT_NAME}} ---
PDFS = [{{PDF_LIST}}]
DB_PATH = "{{DB_FOLDER_NAME}}"
CHUNK_SIZE = {{CHUNK_SIZE}}
CHUNK_OVERLAP = {{CHUNK_OVERLAP}}
MODEL = "{{MODEL_NAME}}"
TEMPERATURE = {{TEMPERATURE}}
MAX_TOKENS = {{MAX_TOKENS}}
K_DOCS = {{K_DOCS}}


def carregar_documentos():
    documentos = []
    for pdf in PDFS:
        loader = PyPDFLoader(pdf)
        documentos.extend(loader.load())
    return documentos


def train():
    documentos = carregar_documentos()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documentos)
    embeddings = OpenAIEmbeddings()

    if os.path.exists(DB_PATH):
        vectordb = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        vectordb.add_documents(chunks)
    else:
        vectordb = FAISS.from_documents(chunks, embeddings)

    vectordb.save_local(DB_PATH)
    print(f"Banco vetorial salvo em '{DB_PATH}' com {len(chunks)} chunks.")


def retrival(pergunta):
    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    docs = vectordb.similarity_search(pergunta, K_DOCS)

    contexto = "\n\n".join([f"Material: {doc.page_content}" for doc in docs])

    prompt = ChatPromptTemplate.from_template(
        "Voce e um {{PERSONA}}.\n"
        "Responda a pergunta do usuario SOMENTE com base no contexto abaixo.\n"
        "Se nao houver informacao suficiente, diga isso claramente.\n\n"
        "Contexto:\n{contexto}\n\n"
        "Pergunta: {pergunta}\n\n"
    )

    llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)
    chain = prompt | llm
    resposta = chain.invoke({'contexto': contexto, 'pergunta': pergunta})
    return resposta.content


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="{{PROJECT_NAME}} - RAG Pipeline")
    parser.add_argument("--treinar", action="store_true", help="Treinar o banco vetorial")
    parser.add_argument("--pergunta", type=str, help="Fazer uma pergunta ao RAG")
    args = parser.parse_args()

    if args.treinar:
        train()
    elif args.pergunta:
        print(retrival(args.pergunta))
    else:
        print("=== {{PROJECT_NAME}} - Assistente RAG ===")
        print("Comandos: 'treinar' para treinar, 'sair' para sair")
        print("Ou digite sua pergunta diretamente.\n")
        while True:
            try:
                entrada = input("Voce: ").strip()
            except (KeyboardInterrupt, EOFError):
                break
            if not entrada:
                continue
            if entrada.lower() == 'sair':
                print("Ate mais!")
                break
            elif entrada.lower() == 'treinar':
                train()
            else:
                print(f"\nAssistente: {retrival(entrada)}\n")
