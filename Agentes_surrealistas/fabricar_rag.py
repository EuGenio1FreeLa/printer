import os
import sys
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"


def banner():
    print("\n" + "=" * 50)
    print("   FABRICADOR DE RAG - Agentes Surrealistas")
    print("=" * 50)
    print("Bem-vindo! Este assistente vai criar um projeto")
    print("RAG completo para voce.")
    print("Valores entre [colchetes] sao os padroes.\n")


def ask(prompt, default=None, required=False, cast=None, validator=None):
    while True:
        if default is not None:
            texto = f"{prompt} [{default}]: "
        else:
            texto = f"{prompt}: "

        resposta = input(texto).strip()

        if not resposta:
            if default is not None:
                resposta = str(default)
            elif required:
                print("  -> Este campo e obrigatorio. Tente novamente.")
                continue

        if cast:
            try:
                resposta = cast(resposta)
            except (ValueError, TypeError):
                print(f"  -> Valor invalido. Esperado: {cast.__name__}")
                continue

        if validator:
            erro = validator(resposta)
            if erro:
                print(f"  -> {erro}")
                continue

        return resposta


def collect_config():
    print("-" * 50)
    print("  IDENTIDADE DO PROJETO")
    print("-" * 50)

    project_name = ask(
        "Nome do projeto",
        required=True,
        validator=lambda v: "Nome nao pode estar vazio" if not v else None
    )

    target_path = ask(
        "Caminho onde o projeto sera criado",
        default=os.getcwd()
    )

    project_description = ask(
        "Descricao curta do projeto",
        default="Projeto RAG"
    )

    print()
    print("-" * 50)
    print("  DOCUMENTOS")
    print("-" * 50)

    pdf_input = ask(
        "Caminhos dos PDFs (separados por virgula)",
        required=True,
        validator=lambda v: "Informe pelo menos um PDF" if not v else None
    )
    pdf_paths = [p.strip() for p in pdf_input.split(",") if p.strip()]

    # Verificar se PDFs existem
    for pdf in pdf_paths:
        if not os.path.exists(pdf):
            print(f"  [AVISO] Arquivo nao encontrado: {pdf}")
            print(f"           Voce pode copiar depois para a pasta do projeto.")

    db_folder_name = ask(
        "Nome da pasta do banco vetorial",
        default="banco_vetorial"
    )

    print()
    print("-" * 50)
    print("  CHUNKING")
    print("-" * 50)

    chunk_size = ask(
        "Tamanho do chunk (chunk_size)",
        default=500,
        cast=int,
        validator=lambda v: "Deve ser maior que 0" if v <= 0 else None
    )

    chunk_overlap = ask(
        "Sobreposicao do chunk (chunk_overlap)",
        default=100,
        cast=int,
        validator=lambda v: (
            "Deve ser >= 0" if v < 0
            else f"Deve ser menor que chunk_size ({chunk_size})" if v >= chunk_size
            else None
        )
    )

    print()
    print("-" * 50)
    print("  MODELO LLM")
    print("-" * 50)

    model_name = ask("Modelo do LLM", default="gpt-4o-mini")

    temperature = ask(
        "Temperatura (0 a 2)",
        default=0,
        cast=float,
        validator=lambda v: "Deve estar entre 0 e 2" if v < 0 or v > 2 else None
    )

    max_tokens = ask(
        "Maximo de tokens na resposta",
        default=500,
        cast=int,
        validator=lambda v: "Deve ser maior que 0" if v <= 0 else None
    )

    k_docs = ask(
        "Quantos documentos similares buscar (k)",
        default=4,
        cast=int,
        validator=lambda v: "Deve ser maior que 0" if v <= 0 else None
    )

    print()
    print("-" * 50)
    print("  PERSONA")
    print("-" * 50)

    persona = ask(
        'Persona do assistente (ex: "especialista em direito")',
        default="assistente especializado"
    )

    return {
        "project_name": project_name,
        "target_path": target_path,
        "project_description": project_description,
        "pdf_paths": pdf_paths,
        "db_folder_name": db_folder_name,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "model_name": model_name,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "k_docs": k_docs,
        "persona": persona,
    }


def show_summary(config):
    pdfs_str = ", ".join(config["pdf_paths"])
    project_dir = os.path.join(config["target_path"], config["project_name"])

    print("\n" + "=" * 50)
    print("   RESUMO DA CONFIGURACAO")
    print("=" * 50)
    print(f"  Projeto:       {config['project_name']}")
    print(f"  Descricao:     {config['project_description']}")
    print(f"  Local:         {project_dir}")
    print(f"  PDFs:          {pdfs_str}")
    print(f"  Banco vetorial:{config['db_folder_name']}")
    print(f"  Chunk size:    {config['chunk_size']}")
    print(f"  Chunk overlap: {config['chunk_overlap']}")
    print(f"  Modelo:        {config['model_name']}")
    print(f"  Temperatura:   {config['temperature']}")
    print(f"  Max tokens:    {config['max_tokens']}")
    print(f"  Docs (k):      {config['k_docs']}")
    print(f"  Persona:       {config['persona']}")
    print("=" * 50)

    resposta = input("\nConfirmar e criar o projeto? [S/n]: ").strip().lower()
    return resposta in ("", "s", "sim", "y", "yes")


def load_template(template_name):
    template_path = TEMPLATES_DIR / template_name
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_template(content, config):
    pdf_filenames = [os.path.basename(p) for p in config["pdf_paths"]]
    pdf_list_str = ", ".join([f'"{f}"' for f in pdf_filenames])

    replacements = {
        "{{PROJECT_NAME}}": str(config["project_name"]),
        "{{PROJECT_DESCRIPTION}}": str(config["project_description"]),
        "{{PDF_LIST}}": pdf_list_str,
        "{{DB_FOLDER_NAME}}": str(config["db_folder_name"]),
        "{{CHUNK_SIZE}}": str(config["chunk_size"]),
        "{{CHUNK_OVERLAP}}": str(config["chunk_overlap"]),
        "{{MODEL_NAME}}": str(config["model_name"]),
        "{{TEMPERATURE}}": str(config["temperature"]),
        "{{MAX_TOKENS}}": str(config["max_tokens"]),
        "{{K_DOCS}}": str(config["k_docs"]),
        "{{PERSONA}}": str(config["persona"]),
    }

    for token, value in replacements.items():
        content = content.replace(token, value)

    return content


def generate_project(config):
    project_dir = os.path.join(config["target_path"], config["project_name"])

    if os.path.exists(project_dir):
        print(f"\n[AVISO] A pasta '{project_dir}' ja existe.")
        resposta = input("Sobrescrever arquivos? [s/N]: ").strip().lower()
        if resposta not in ("s", "sim", "y", "yes"):
            print("Operacao cancelada.")
            return
    else:
        os.makedirs(project_dir, exist_ok=True)

    # Mapear template -> arquivo de saida
    files_map = {
        "app_template.py": "app.py",
        "view_faiss_template.py": "view_faiss.py",
        "grafico_template.py": "grafico.py",
        "requirements_template.txt": "requirements.txt",
        "env_template.txt": ".env",
        "readme_template.md": "README.md",
    }

    print("\nGerando arquivos...")

    for template_name, output_name in files_map.items():
        content = load_template(template_name)
        rendered = render_template(content, config)
        output_path = os.path.join(project_dir, output_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"  [OK] {output_name}")

    # Copiar PDFs para o projeto
    print("\nCopiando PDFs...")
    for pdf_path in config["pdf_paths"]:
        if os.path.exists(pdf_path):
            dest = os.path.join(project_dir, os.path.basename(pdf_path))
            shutil.copy2(pdf_path, dest)
            print(f"  [OK] {os.path.basename(pdf_path)}")
        else:
            print(f"  [PULADO] {pdf_path} (nao encontrado)")

    # Criar .gitignore
    gitignore_path = os.path.join(project_dir, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(".env\n__pycache__/\n*.pyc\n")
        f.write(f"{config['db_folder_name']}/\n")
        f.write("faiss_exportado.json\n")
    print("  [OK] .gitignore")

    print("\n" + "=" * 50)
    print("   PROJETO CRIADO COM SUCESSO!")
    print("=" * 50)
    print(f"\n  Local: {project_dir}\n")
    print("  Proximos passos:")
    print(f"  1. cd \"{project_dir}\"")
    print("  2. pip install -r requirements.txt")
    print("  3. Edite o .env com sua chave da OpenAI")
    print("  4. python app.py --treinar")
    print("  5. python app.py --pergunta \"Sua pergunta\"")
    print("  6. Ou: python app.py  (modo interativo)\n")


def main():
    banner()
    try:
        config = collect_config()
        if show_summary(config):
            generate_project(config)
        else:
            print("\nOperacao cancelada pelo usuario.")
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperacao cancelada.")
        sys.exit(0)


if __name__ == "__main__":
    main()
