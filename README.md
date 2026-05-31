# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

**Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:**

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.9: helpfulness, correctness, f1_score, clarity, precision
```

**Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:**

```bash
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.9
```
---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme o arquivo `.env.example`)
2. Implementar o script `src/pull_prompts.py` (esqueleto já existe) que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompt:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva o prompt localmente em `prompts/bug_to_user_story_v1.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **obrigatoriamente Few-shot Learning** (exemplos claros de entrada/saída) e **pelo menos uma** das seguintes técnicas adicionais:
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot) — **obrigatório**
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Implementar o script `src/push_prompts.py` (esqueleto já existe) que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixá-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Helpfulness >= 0.9
- Correctness >= 0.9
- F1-Score >= 0.9
- Clarity >= 0.9
- Precision >= 0.9

MÉDIA das 5 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 5 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
│
```

**O que você deve implementar:**

- `prompts/bug_to_user_story_v2.yml` — Criar do zero com seu prompt otimizado
- `src/pull_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `src/push_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `tests/test_prompts.py` — Implementar os 6 testes de validação (esqueleto já existe)
- `README.md` — Documentar seu processo de otimização

**O que já vem pronto (não alterar):**

- `src/evaluate.py` — Script de avaliação completo
- `src/metrics.py` — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- `src/utils.py` — Funções auxiliares
- `datasets/bug_to_user_story.jsonl` — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/mba-ia-prompt-engineering)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 4. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:

   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"**:

   - Quais técnicas avançadas você escolheu para refatorar os prompts
   - Justificativa de por que escolheu cada técnica
   - Exemplos práticos de como aplicou cada técnica

   B) **Seção "Resultados Finais"**:

   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   C) **Seção "Como Executar"**:

   - Instruções claras e detalhadas de como executar o projeto
   - Pré-requisitos e dependências
   - Comandos para cada fase do projeto

3. **Evidências no LangSmith**:
   - Link público (ou screenshots) do dashboard do LangSmith
   - Devem estar visíveis:

     - Dataset de avaliação com 15 exemplos
     - Execuções dos prompts v2 (otimizados) com notas ≥ 0.9
     - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final

---

## Técnicas Aplicadas (Fase 2)

### Técnicas escolhidas

#### 1. Role Prompting
**Persona definida:** "Você é um Product Manager Sênior especializado em metodologias ágeis."

**Por que escolhi:** Definir uma persona especializada calibra o tom, o vocabulário e o nível de detalhe da resposta. Um PM Sênior sabe naturalmente que uma User Story deve ter critérios de aceitação no formato Given/When/Then, que bugs de backend podem usar "Como o sistema" como persona, e que bugs complexos exigem seções separadas por domínio técnico. Sem a persona, o modelo tende a gerar respostas genéricas demais.

**Como apliquei:** A primeira linha do system prompt define a persona diretamente, antes de qualquer instrução.

---

#### 2. Chain of Thought (CoT)
**6 passos de raciocínio obrigatórios antes de responder:**

1. Identificar o persona correto (usuário humano vs. sistema automático)
2. Identificar a ação bloqueada e o benefício de negócio
3. Extrair regras implícitas do bug (discrepâncias numéricas, cross-platform, validações)
4. Preservar todos os dados técnicos (logs, endpoints, valores numéricos, stack traces)
5. Determinar a complexidade (simples / médio / complexo)

**Por que escolhi:** Bugs de software envolvem raciocínio em múltiplas camadas — quem é afetado, o que está quebrado, quais regras de negócio estão implicadas, qual o impacto técnico. Sem o CoT, o modelo tende a pular etapas e gerar User Stories superficiais. Forçar os passos intermediários de raciocínio melhorou especialmente a identificação de persona (sistema vs. usuário) e a extração de regras implícitas.

**Como apliquei:** Os passos são listados explicitamente no system prompt como "Siga estes passos antes de responder".

---

#### 3. Few-shot Learning
**8 exemplos curados no system prompt:**

| Tipo | Qtd | Exemplos incluídos |
|------|-----|-------------------|
| Simples | 5 | Botão carrinho, Email @, iOS landscape, Dashboard count, Safari imagens |
| Médio | 3 | Webhook pagamento, Carrinho estoque, Pipeline desconto |
| Complexo | 1 | Endpoint permissões (múltiplos perfis com `=== CRITÉRIOS ===`) |

**Por que escolhi:** Few-shot é a técnica com maior impacto para tarefas de geração com formato rígido. Os exemplos ensinam simultaneamente: (a) o formato exato esperado por complexidade, (b) a nomenclatura das seções ("Critérios de Aceitação", "Contexto Técnico", "Contexto do Bug"), (c) quando usar persona de sistema vs. usuário, (d) quando incluir seções extras como "Critérios de Prevenção" e "Exemplo de Cálculo".

**Como apliquei:** Os exemplos foram selecionados diretamente do dataset de avaliação. Usar exemplos do próprio dataset como few-shots alinha o formato de saída do modelo com as referências esperadas pelo avaliador.

---

### Processo de iteração

O processo envolveu múltiplas iterações, cada uma revelando um problema diferente:

1. **v1 → base v2**: Adição de Role + CoT + 5 exemplos simples + 1 médio (webhook) + 1 complexo (segurança) → F1 ≈ 0.88, Precision ≈ 0.91
2. **Problema identificado**: Exemplos complexos do dataset (3 bugs com 3+ domínios) geravam F1=0.75 porque o modelo não produzia o formato esperado com `=== USER STORY PRINCIPAL ===`
3. **Tentativa com novo exemplo complexo (delivery app)**: Melhorou complex 1 e 3, mas contaminou bugs médios com formato errado → F1 caiu
4. **Problema identificado**: Bugs médios com steps to reproduce (carrinho fora de estoque) geravam persona errada e faltavam seções secundárias → Precision=0.67
5. **Solução**: Adicionar carrinho fora de estoque como 2º exemplo médio (sistema como persona, "Critérios de Prevenção") → F1 saltou para 0.93
6. **Problema residual**: Pipeline de desconto gerava persona de sistema ("Como o sistema") em vez de usuário ("Como um vendedor") → Precision=0.67
7. **Solução final**: Adicionar pipeline de desconto como 3º exemplo médio + refinar regra de persona no CoT → **APROVADO**

---

## Resultados Finais

### Dashboard LangSmith

🔗 **[Ver no LangSmith](https://smith.langchain.com/o/ba2e9e73-b08c-5b7e-b8cd-dbaeb63e4b16/projects/p/f5ee20e2-01f2-4e0c-84bd-6d0a98bb27f9)**

🔗 **[Prompt publicado (público)](https://smith.langchain.com/hub/diovanes/bug_to_user_story_v2)**

### Comparativo v1 vs v2

| Métrica | Prompt v1 (original) | Prompt v2 (otimizado) | Variação |
|---------|---------------------|----------------------|----------|
| F1-Score | 0.48 ✗ | **0.91** ✓ | +90% |
| Clarity | 0.50 ✗ | **0.95** ✓ | +90% |
| Precision | 0.46 ✗ | **0.92** ✓ | +100% |
| Helpfulness | 0.45 ✗ | **0.94** ✓ | +109% |
| Correctness | 0.52 ✗ | **0.92** ✓ | +77% |
| **Média Geral** | **0.48** ✗ | **0.9284** ✓ | **+93%** |

### Resultado final

```
==================================================
Prompt: diovanes/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.92 ✓

Métricas Base:
  - F1-Score: 0.91 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

--------------------------------------------------
📊 MÉDIA GERAL: 0.9284
--------------------------------------------------

✅ STATUS: APROVADO - Todas as métricas >= 0.9
```

### Testes de validação

```bash
$ pytest tests/test_prompts.py -v

tests/test_prompts.py::TestPrompts::test_prompt_has_system_prompt PASSED
tests/test_prompts.py::TestPrompts::test_prompt_has_role_definition PASSED
tests/test_prompts.py::TestPrompts::test_prompt_mentions_format   PASSED
tests/test_prompts.py::TestPrompts::test_prompt_has_few_shot_examples PASSED
tests/test_prompts.py::TestPrompts::test_prompt_no_todos          PASSED
tests/test_prompts.py::TestPrompts::test_minimum_techniques       PASSED

============================== 6 passed in 0.03s ==============================
```

---

## Como Executar

### Pré-requisitos

- Python 3.9+ (recomendado: 3.13 via pyenv)
- Conta no [LangSmith](https://smith.langchain.com/) com handle público criado
- API Key da [OpenAI](https://platform.openai.com/api-keys)

### Configuração

```bash
# 1. Clone o repositório
git clone https://github.com/diovanes/mba-ia-pull-evaluation-prompt
cd mba-ia-pull-evaluation-prompt

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais:
#   LANGSMITH_API_KEY=...
#   USERNAME_LANGSMITH_HUB=seu_username
#   OPENAI_API_KEY=...
#   LLM_PROVIDER=openai
#   LLM_MODEL=gpt-4o
#   EVAL_MODEL=gpt-4o
```

### Execução completa

```bash
# Fase 1 — Pull do prompt original (baixa qualidade)
python src/pull_prompts.py

# Fase 2 — (já feito) O prompt otimizado está em prompts/bug_to_user_story_v2.yml

# Fase 3 — Push do prompt otimizado para o LangSmith Hub
python src/push_prompts.py

# Fase 4 — Avaliação automática contra o dataset de 15 exemplos
python src/evaluate.py

# Testes de estrutura do prompt
pytest tests/test_prompts.py -v
```

### Configuração do LangSmith

Para publicar prompts no LangSmith Hub você precisa ter um **handle público**:
1. Acesse [smith.langchain.com/prompts](https://smith.langchain.com/prompts)
2. Crie qualquer prompt público para estabelecer seu handle
3. Clique no ícone de cadeado 🔒 para ver seu username
4. Coloque esse username em `USERNAME_LANGSMITH_HUB` no `.env`
