Spec Driven Development (SDD) apresentada no material, organizada em formato de prompts prontos para você configurar seus agentes no Visual Studio Code.
O segredo do método é tratar o processo como um funil para gerenciar a "Janela de Contexto" (memória da IA). Você deve dividir o trabalho em três etapas e, obrigatoriamente, limpar a memória entre elas.
Abaixo estão os prompts detalhados para cada agente ou etapa:

---

Etapa 1: O Pesquisador (Geração do PRD)
Contexto: Nesta fase, a IA deve varrer a base de código e a internet para entender o terreno. O objetivo não é codar ainda, mas sim filtrar o que é útil do que é inútil.
Prompt para o Agente de Pesquisa:
Aja como um Engenheiro de Software Sênior focado em planejamento técnico. Eu preciso implementar a funcionalidade: [INSIRA AQUI A DESCRIÇÃO DO QUE VOCÊ QUER FAZER].
Sua tarefa é realizar uma pesquisa profunda antes de escrevermos qualquer código. Siga rigorosamente os passos abaixo:

1. Análise de Impacto Interno: Pesquise em toda a nossa base de código atual para identificar quais arquivos serão afetados por essa nova funcionalidade. Liste apenas os relevantes.
2. Busca por Padrões (DRY): Verifique se já existem padrões de implementação similares no projeto (ex: componentes de UI, fluxos de autenticação, conexões de banco) para que possamos reutilizá-los. Não quero reinventar a roda nem duplicar código existente.
3. Contexto Externo e Documentação: Se a tarefa envolver bibliotecas externas (ex: Stripe, NextAuth, Resend), leia a documentação oficial mais recente ou busque exemplos de implementação (snippets) confiáveis na web ou em repositórios conhecidos.
4. Saída (Output): Com base em tudo o que você leu, crie um arquivo chamado prd.md (Product Requirements Document).
   O prd.md deve conter:
   • Resumo do Objetivo: O que vamos construir.
   • Arquivos Relevantes: Lista dos arquivos da base de código que serão tocados.
   • Documentação: Trechos importantes das documentações lidas.
   • Code Snippets: Padrões de código encontrados (internos ou externos) que servirão de guia.
   • Filtro: Não inclua informações inúteis ou arquivos que não serão alterados.

---

⚠️ Ação Obrigatória do Usuário: Após a geração do prd.md, execute o comando de limpar o contexto (ex: /clear ou reiniciar a sessão do agente). O próximo agente deve ler apenas o arquivo prd.md.

---

Etapa 2: O Arquiteto (Geração da Spec)
Contexto: Agora que temos o resumo da pesquisa (prd.md), este agente deve criar um plano tático de batalha. O objetivo é eliminar ambiguidades para que o programador não precise "adivinhar" nada.
Prompt para o Agente de Especificação:
Leia atentamente o arquivo prd.md que foi gerado na etapa anterior. Ele contém todo o contexto necessário sobre a funcionalidade que vamos implementar.
Com base nesse documento, sua tarefa é criar um plano tático de implementação extremamente detalhado. Gere um arquivo chamado spec.md.
O spec.md deve conter explicitamente:

1. Arquivos a Criar: A lista exata de novos arquivos que devem ser criados (com seus caminhos/paths completos).
2. Arquivos a Modificar: A lista exata de arquivos existentes que serão alterados.
3. Instruções Detalhadas por Arquivo: Para cada arquivo listado, descreva o que deve ser feito.
   ◦ Quais funções criar?
   ◦ Quais importações adicionar?
   ◦ Qual lógica alterar?
4. Pseudocódigo e Snippets: Inclua os trechos de código (code snippets) que foram identificados no PRD para garantir que a implementação siga os padrões do projeto.
   Regras de Ouro:
   • Evite "overengineering": escolha a solução mais simples e direta.
   • Seja tático: não deixe margem para interpretação. Defina nomes de variáveis e funções se necessário.
   • Modularização: garanta que o código não misture responsabilidades (ex: não misturar lógica de banco de dados com interface no mesmo arquivo se não for o padrão).

---

⚠️ Ação Obrigatória do Usuário: Após a geração do spec.md, execute novamente o comando de limpar o contexto. O próximo agente deve ler apenas o arquivo spec.md e ter a memória livre para focar 100% em codar.

---

Etapa 3: O Desenvolvedor (Implementação)
Contexto: Esta é a etapa final. Como o agente tem um "mapa" claro (spec.md) e a memória limpa, a chance de alucinação, erros ou repetição de código diminui drasticamente (One Shot).
Prompt para o Agente de Implementação:
Leia o arquivo spec.md. Este é o seu plano de implementação definitivo.
Como sua janela de contexto está limpa e focada apenas neste plano, utilize sua capacidade máxima para escrever um código de alta qualidade, seguindo estas diretrizes:

1. Execução Rigorosa: Implemente exatamente o que está descrito na spec. Crie e modifique apenas os arquivos listados.
2. Consistência: Utilize os padrões e snippets fornecidos no plano. Não tente criar soluções "criativas" se o plano já define como fazer.
3. Simplicidade: Não adicione complexidade desnecessária. Escreva um código limpo, modular e fácil de dar manutenção.
4. One Shot: Seu objetivo é fazer o código funcionar na primeira tentativa, confiando nas documentações e caminhos definidos na spec.
   Pode começar a codar.

---

Resumo do Fluxo para seus Agentes no VS Code:

1. Agente 1 (Input: Sua ideia): Pesquisa -> Gera prd.md.
2. Ação: Reset de Memória.
3. Agente 2 (Input: prd.md): Planeja -> Gera spec.md.
4. Ação: Reset de Memória.
5. Agente 3 (Input: spec.md): Executa -> Gera o Código Final.
