# Agents Studies

Repositório dedicado a anotar, explorar e fixar estudos em Agentes/Sistema Multiagentes de I.A.

---

## Visão Geral do Repositório

Este projeto é um estudo abrangente sobre sistemas de agentes de Inteligência Artificial, abrangendo desde arquiteturas clássicas até frameworks modernos e padrões de projeto. O objetivo é construir uma base sólida de conhecimento sobre como projetar, implementar e orquestrar agentes de IA.

---

## Estrutura de Diretórios

```text
agents_studies/
├── arquiteturas_classicas/      # Estudo das arquiteturas fundamentais de agentes
├── frameworks_e_ferramentas/   # Frameworks e ferramentas para construção de agentes
├── padroes_projeto/            # Padrões de projeto para sistemas de agentes
├── .env.example                # Modelo de variáveis de ambiente
├── requirements.txt            # Dependências Python do projeto
└── README.md                   # Este arquivo
```

---

##  Arquiteturas Clássicas

Pasta: [`arquiteturas_classicas/`](arquiteturas_classicas)

Estudo das arquiteturas fundamentais de agentes de IA, desde as mais simples até as mais sofisticadas.

### Arquiteturas Incluídas

| Arquitetura | Descrição |
|-------------|-----------|
| **Reflexiva** | Agentes que tomam decisões baseados apenas no estado atual do ambiente. Sem memória, sem aprendizado, puramente reativos. |
| **Baseada em Modelo** | Agentes que mantêm uma representação interna do mundo (memória), permitindo decisões mais inteligentes baseadas em histórico. |
| **Híbrida** | Combinação da rapidez da arquitetura reflexiva com a inteligência da arquitetura baseada em modelo. Tipicamente possui 3 camadas: reflexiva, deliberativa e de coordenação. |

### Quando Usar Cada Arquitetura?

A escolha depende de fatores como:
- Complexidade do ambiente
- Dados disponíveis e necessários
- Custos computacionais
- Requisitos de latência
- Necessidade de memória e contexto

---

## Frameworks e Ferramentas

Pasta: [`frameworks_e_ferramentas/`](frameworks_e_ferramentas)

Implementações práticas utilizando frameworks modernos para construção de agentes.

### Frameworks Estudados

| Framework | Tipo | Descrição |
|-----------|------|-----------|
| **LangChain** | Single Agent | Framework para construção de agentes via código Python. Fornece classes para criar pipelines envolvendo LLMs com controle total sobre cada detalhe. |
| **CrewAI** | Multi-Agent | Framework focado em orquestração e gerenciamento de sistemas multiagentes. Construído sobre o LangChain, permite criar "times" de agentes com papéis definidos. |
| **LangGraph** | Graph-Based | Framework orientado a grafos para workflows complexos com múltiplos caminhos, loops e ramificações. Cada nó é um agente ou função; as arestas definem o fluxo de execução. |

### Projetos Implementados

- **[Agente Simples LangChain](frameworks_e_ferramentas/agente_simples_langchain/)**: Agente de vendas inteligente utilizando ReAct (Reasoning + Acting) com ferramentas personalizadas.
  - Busca flexível de produtos (fuzzy search)
  - Cálculos matemáticos precisos
  - Memória de conversa
  - Tratamento robusto de erros

- **[Multi-Agentes CrewAI](frameworks_e_ferramentas/multi_agentes_crewAI/)**: Sistema multiagentes para análise de investimentos em ações.
  - Agente Pesquisador (dados técnicos)
  - Agente Analista de Notícias (sentimento de mercado)
  - Agente Consultor (recomendação final)

- **[Auditoria de Segurança LangGraph](frameworks_e_ferramentas/agentes_langgraph/)**: Workflow de auditoria de repositórios GitHub com padrão Fan-Out/Fan-In.
  - Análise estática de código (SAST)
  - Verificação de dependências (SCA)
  - Análise de documentação

---

## RAG (Retrieval-Augmented Generation)

Pasta: [`rag/`](rag)

Pipeline de perguntas e respostas sobre documentos PDF locais. Usa Qdrant como banco vetorial, embeddings multilíngues (E5) e LLM via OpenRouter. Interface construída com Streamlit.

- **[RAG com Qdrant](rag/)**: Ingestão de PDFs e consulta via busca semântica + geração de resposta.

---

##  Padrões de Projeto

Pasta: [`padroes_projeto/`](padroes_projeto)

Padrões recorrentes na construção de agentes e sistemas multiagentes. São como "formas de organizar agentes" para resolver problemas comuns de design.

### Padrões Estudados

| Padrão | Descrição |
|--------|-----------|
| **Planejador-Executor (Planner-Executor)** | Separação entre agent que planeja ações e agente que as executa. |
| **Supervisor-Trabalhador (Supervisor-Worker)** | Um agente supervisor coordena múltiplos agentes trabalhadores especializados. |
| **Agente com Ferramentas/Skills** | Agentes equipados com ferramentas específicas para выполнять tarefas específicas. |

---

## Como Utilizar Este Repositório

### Pré-requisitos

- Python 3.10 ou superior
- Chaves de API (consulte `.env.example`)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/agents_studies.git
cd agents_studies

# Crie e ative o ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Instale as dependências
uv pip install -r requirements.txt
```

### Configuração

1. Copie o arquivo `.env.example` para `.env`
2. Configure suas chaves de API conforme necessário

### Executando os Projetos

Cada subdiretório possui seu próprio README com instruções específicas. Consulte-os para detalhes de execução.

---

## Conceitos Fundamentais

### O que é um Agente de IA?

Um agente de IA é um sistema computacional capaz de:
1. **Perceber** o ambiente através de sensores ou entradas
2. **Decidir** ações baseadas em seu conhecimento
3. **Executar** ações que afetam o ambiente
4. **Aprender** com as experiências (opcional, dependendo da arquitetura)

### Sistema Multiagentes (MAS)

Um Sistema Multiagentes é um sistema composto por múltiplos agentes que:
- Comunicam-se entre si
- Cooperam ou competem para atingir objetivos
- Podem ter papéis especializados
- São coordenados por um orquestrador

### Por que usar Multi-Agentes?

- **Divisão de responsabilidades**: Cada agente especialista em uma tarefa
- **Paralelização**: Múltiplas tarefas podem ser executadas simultaneamente
- **Escalabilidade**: Adicionar novos agentes é mais simples que modificar um monólito
- **Robustez**: Falha de um agente não derruba todo o sistema

---

##  Roadmap de Estudos

- [x] Arquiteturas clássicas de agentes
- [x] LangChain para agentes únicos
- [x] CrewAI para sistemas multiagentes
- [x] LangGraph para workflows orientados a grafos
- [x] RAG com Qdrant
- [x] Integração com Vector Databases (Qdrant)
- [x] Padrão Planner-Executor
- [x] Padrão ReAct com Agno
- [ ] Padrão Supervisor-Worker
- [ ] Agentes com LLMs locais
- [ ] Agentes com memória persistente

---

##  Contribuições

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou enviar pull requests.


