# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

Gerado pelo **Fabricador de RAG - Agentes Surrealistas**.

## Como usar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar chave da OpenAI
Edite o arquivo `.env` e coloque sua chave:
```
OPENAI_API_KEY=sk-sua-chave-aqui
```

### 3. Treinar o banco vetorial
```bash
python app.py --treinar
```

### 4. Fazer perguntas
Via argumento:
```bash
python app.py --pergunta "Sua pergunta aqui"
```

Ou modo interativo:
```bash
python app.py
```

### 5. Inspecionar o banco vetorial
```bash
python view_faiss.py
```
Gera o arquivo `faiss_exportado.json` com o conteudo dos chunks e vetores.

### 6. Visualizar embeddings
```bash
python grafico.py
```
Gera o arquivo `embeddings_visualizacao.png` com o grafico t-SNE dos vetores.

## Configuracao

| Parametro | Valor |
|-----------|-------|
| Chunk size | {{CHUNK_SIZE}} |
| Chunk overlap | {{CHUNK_OVERLAP}} |
| Modelo | {{MODEL_NAME}} |
| Temperatura | {{TEMPERATURE}} |
| Max tokens | {{MAX_TOKENS}} |
| Docs similares (k) | {{K_DOCS}} |
| Persona | {{PERSONA}} |
| Banco vetorial | {{DB_FOLDER_NAME}} |

## Importante
- Nunca commite o arquivo `.env` no git
- Adicione `.env` ao seu `.gitignore`
