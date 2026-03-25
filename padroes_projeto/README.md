# Padrões de Projeto

"Além das arquiteturas gerais, existem padrões de projeto recorrentes na construção de agentes e sistemas multiagentes. Esses padrões são como “formas de organizar agentes” para resolver problemas comuns de design, distribuindo responsabilidades entre módulos ou facilitando a cooperação."

## 1 - Planejador-Executor (Planner-Executor)

Separacao entre o agente que planeja acoes e o agente que as executa. O Planejador gera um roteiro e o Executor percorre cada passo, podendo usar ferramentas. Ideal para tarefas multi-etapas onde o caminho completo nao e conhecido de antemao.

Projeto: [LANGGRAPH-PLANNER-EXECUTOR-PesquisadorDeIA](LANGGRAPH-PLANNER-EXECUTOR-PesquisadorDeIA/)

## 2 - Supervisor-Trabalhador (Supervisor-Worker)

- Em breve...

## 3 - Agente com Ferramentas/Skills (ReAct)

Agente equipado com ferramentas especificas para realizar acoes no mundo real. O padrao ReAct (Reasoning + Acting) guia o agente a raciocinar sobre qual ferramenta usar antes de agir.

Projeto: [AGNO-ReAct-ConsultorDeVendas](AGNO-ReAct-ConsultorDeVendas/)