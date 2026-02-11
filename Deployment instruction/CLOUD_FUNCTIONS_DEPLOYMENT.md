# Manual de Deploy - Firebase Cloud Functions

## Visao Geral

Este documento explica como fazer deploy das Cloud Functions do projeto Lampada. As funcoes rodam no **Google Cloud Run** (2nd gen) na regiao `southamerica-east1` (Sao Paulo).

---

## Pre-requisitos

### 1. Ferramentas Necessarias

```bash
# Node.js 20+
node --version  # deve mostrar v20.x.x

# Firebase CLI
npm install -g firebase-tools
firebase --version  # deve mostrar 13.x.x ou superior

# Login no Firebase
firebase login
```

### 2. Configuracao do Projeto

```bash
# Navegar para a pasta do projeto
cd "x:\DevOps\ISM - O Trecho\Lampada"

# Verificar projeto ativo
firebase projects:list
firebase use symbolic-wind-481516-b6  # nosso projeto
```

---

## Estrutura das Functions

```
Lampada/
└── functions/
    ├── src/
    │   └── index.ts      # Codigo fonte das funcoes
    ├── lib/
    │   └── index.js      # Codigo compilado (gerado pelo build)
    ├── package.json      # Dependencias
    └── tsconfig.json     # Config TypeScript
```

### Funcoes Disponiveis

| Funcao | Descricao | Autenticacao |
|--------|-----------|--------------|
| `chatWithOracle` | IA conversacional | Usuario |
| `submitDailyMetrics` | Salvar metricas + XP | Usuario |
| `completeMission` | Completar missao + XP | Usuario |
| `completeProject` | Completar projeto + XP | Usuario |
| `markClassComplete` | Completar aula + XP | Usuario |
| `approveContent` | Aprovar conteudo | Admin |
| `rejectContent` | Rejeitar conteudo | Admin |
| `approveComment` | Aprovar comentario | Admin |
| `rejectComment` | Rejeitar comentario | Admin |
| `submitLead` | Formulario de lead | Publico |
| `getLeadStats` | Estatisticas de leads | Admin |
| `createCheckoutSession` | Criar checkout Stripe | Usuario |
| `stripeWebhook` | Webhook do Stripe | Publico |
| `setAdminRole` | Definir admin | Super Admin |
| `deleteUserAccount` | Excluir conta | Usuario |

---

## Comandos de Deploy

### Build (Compilar TypeScript)

**SEMPRE faca build antes de deploy!**

```bash
cd functions
npm run build
```

Isso compila `src/index.ts` para `lib/index.js`.

### Deploy Completo

```bash
# Da pasta Lampada (nao functions!)
cd "x:\DevOps\ISM - O Trecho\Lampada"

# Deploy de TODAS as funcoes
firebase deploy --only functions
```

### Deploy de Funcoes Especificas

```bash
# Uma funcao
firebase deploy --only functions:chatWithOracle

# Multiplas funcoes
firebase deploy --only functions:approveContent,functions:rejectContent,functions:approveComment

# Por grupo (se definido)
firebase deploy --only functions:admin
```

### Deploy Apenas Firestore Rules

```bash
firebase deploy --only firestore:rules
```

### Deploy Completo (Functions + Rules + Hosting)

```bash
firebase deploy
```

---

## Fluxo de Deploy Recomendado

```
1. Fazer alteracoes no codigo
         ↓
2. cd functions && npm run build
         ↓
3. Verificar se compilou sem erros
         ↓
4. cd .. && firebase deploy --only functions
         ↓
5. Verificar logs no Console Firebase
         ↓
6. Testar funcionalidade no app
```

---

## Problemas Comuns e Solucoes

### 1. Quota Exceeded (Erro de Cota)

**Erro:**
```
Container Healthcheck failed. Quota exceeded for total allowable CPU per project per region.
```

**Causa:**
- Google Cloud Run tem limites de CPU por projeto/regiao
- Ao deployar muitas funcoes simultaneamente, o limite e atingido

**Solucao:**
```bash
# Esperar 1-2 horas para a cota resetar

# OU deployar em lotes menores
firebase deploy --only functions:funcao1,functions:funcao2

# OU deployar funcoes que falharam individualmente
firebase deploy --only functions:completeMission
firebase deploy --only functions:createCheckoutSession
```

**Prevencao:**
- Evitar deploy de todas as funcoes de uma vez
- Deployar em horarios de baixo uso
- Considerar upgrade de billing para quotas maiores

---

### 2. Build Error (Erro de Compilacao)

**Erro:**
```
error TS2304: Cannot find name 'xxx'
```

**Solucao:**
```bash
cd functions
npm install           # Reinstalar dependencias
npm run build         # Tentar novamente
```

---

### 3. Function Not Found

**Erro:**
```
Function xxx not found
```

**Causa:**
- Nome da funcao incorreto
- Funcao nao foi exportada no index.ts
- Build nao foi feito apos adicionar funcao

**Solucao:**
```bash
# Verificar se funcao esta exportada
cat functions/src/index.ts | grep "export const nomeDaFuncao"

# Refazer build
cd functions && npm run build
```

---

### 4. Permission Denied

**Erro:**
```
Error: HTTP Error: 403, The caller does not have permission
```

**Solucao:**
```bash
# Re-autenticar
firebase logout
firebase login

# Verificar projeto
firebase use symbolic-wind-481516-b6
```

---

### 5. Timeout During Deploy

**Erro:**
```
Function failed to deploy within the deadline
```

**Solucao:**
```bash
# Aumentar timeout no deploy
firebase deploy --only functions --timeout 600s

# Ou deployar funcoes individualmente
```

---

## Monitoramento

### Ver Logs em Tempo Real

```bash
# Todas as funcoes
firebase functions:log

# Funcao especifica
firebase functions:log --only chatWithOracle

# Ultimas 100 linhas
firebase functions:log -n 100
```

### Console Firebase

1. Acesse: https://console.firebase.google.com
2. Selecione o projeto `symbolic-wind-481516-b6`
3. Va em **Functions** no menu lateral
4. Clique em uma funcao para ver:
   - Invocacoes
   - Erros
   - Latencia
   - Logs

### Google Cloud Console

Para logs mais detalhados:
1. Acesse: https://console.cloud.google.com
2. Va em **Cloud Run** > Servicos
3. Selecione a funcao
4. Aba **Logs**

---

## Variaveis de Ambiente e Secrets

### Secrets Configurados

| Secret | Descricao |
|--------|-----------|
| `GEMINI_API_KEY` | API do Google Gemini (IA) |
| `STRIPE_SECRET_KEY` | Chave secreta Stripe |
| `STRIPE_WEBHOOK_SECRET` | Webhook secret Stripe |
| `RESEND_API_KEY` | API de emails |

### Ver Secrets

```bash
firebase functions:secrets:access GEMINI_API_KEY
```

### Adicionar/Atualizar Secret

```bash
firebase functions:secrets:set NOVA_CHAVE
# Digite o valor quando solicitado
```

---

## Checklist Pre-Deploy

- [ ] Codigo testado localmente
- [ ] `npm run build` sem erros
- [ ] Verificar se secrets necessarios estao configurados
- [ ] Commit das alteracoes no Git
- [ ] Verificar se nao ha deploy em andamento

---

## Checklist Pos-Deploy

- [ ] Verificar se todas funcoes estao "Active" no Console
- [ ] Testar funcionalidade principal no app
- [ ] Verificar logs para erros
- [ ] Comunicar equipe sobre mudancas

---

## Contatos

**Problemas tecnicos:**
- Verificar este manual
- Consultar documentacao Firebase: https://firebase.google.com/docs/functions
- Abrir issue no repositorio

**Erros de cota persistentes:**
- Aguardar reset automatico (1-2h)
- Considerar upgrade do plano Blaze

---

## Historico de Deploys

| Data | Funcoes | Status | Notas |
|------|---------|--------|-------|
| 2026-01-17 | Todas | Parcial | 5 funcoes com erro de cota |
| 2026-01-17 | Firestore Rules | OK | Rules para courses/conteudo |

---

*Ultima atualizacao: Janeiro 2026*
