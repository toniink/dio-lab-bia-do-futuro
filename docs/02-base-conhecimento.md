# Base de Conhecimento

## Dados Utilizados

O agente utiliza de forma integrada todos os arquivos estruturados na pasta `data/` para compor uma visão 360° do cliente, permitindo uma atuação contextualizada e proativa.

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Utilizado para dar memória de longo prazo ao agente, permitindo relembrar dúvidas passadas do cliente (como o interesse recente pelo Tesouro Selic) e demonstrar empatia. |
| `perfil_investidor.json` | JSON | Funciona como o núcleo de regras de negócio. Define as metas do cliente (completar reserva e apartamento), tolerância a risco e capacidade financeira. |
| `produtos_financeiros.json` | JSON | Funciona como o catálogo de prateleira da instituição, onde o agente busca as opções de investimento de risco compatível para recomendar de forma consultiva. |
| `transacoes.csv` | CSV | Analisado dinamicamente para calcular o fluxo de caixa mensal (receitas vs. despesas), identificar o saldo livre atual e alertar sobre limites de gastos por categoria. |

---

## Adaptações nos Dados

Os dados originais fornecidos foram padronizados e higienizados. Os arquivos brutos de formato CSV foram estruturados com cabeçalhos claros (`data`, `canal`, `tema`, `resumo`, `resolvido` para atendimentos e `data`, `descricao`, `categoria`, `valor`, `tipo` para transações), além de terem seus separadores corrigidos para vírgulas, garantindo uma leitura limpa via biblioteca Pandas (`pd.read_csv`). Nenhuma informação financeira do cliente João Silva foi alterada, mantendo o realismo do cenário.

---

## Estratégia de Integração

### Como os dados são carregados?
No início da execução da aplicação (via Streamlit), um módulo Python executa uma rotina de carga de dados. O arquivo `perfil_investidor.json` e a lista de `produtos_financeiros.json` são carregados diretamente na memória como dicionários. Já os arquivos `transacoes.csv` e `historico_atendimento.csv` são lidos como DataFrames do Pandas. A partir daí, o script calcula automaticamente métricas consolidadas (como total gasto no mês, saldo atual disponível e progresso percentual da meta) para não sobrecarregar o contexto da LLM com dados brutos desnecessários.

### Como os dados são usados no prompt?
A estratégia adota uma abordagem híbrida:
1. **Dados Fixos de Contexto:** O perfil básico do cliente (nome, idade, objetivos principais e progresso das metas) é injetado diretamente no `System Prompt` para consolidar a persona e o conhecimento de fundo sobre o usuário.
2. **Consultas Dinâmicas (RAG):** O histórico completo de transações e produtos financeiros não é enviado de forma integral. Quando o cliente interage ou quando um gatilho de gasto é acionado, o agente filtra dinamicamente as linhas relevantes do Pandas (ex: apenas transações de outubro ou apenas produtos de baixo risco) e injeta esse recorte formatado como uma mensagem de contexto de suporte no prompt da LLM antes de gerar a resposta.

---

## Exemplo de Contexto Montado

Abaixo está o exemplo de como o módulo de integração Python consolida e formata os dados brutos da pasta `data/` em um bloco de texto estruturado para ser injetado no prompt da LLM:

```text
==================================================
CONTEXTO DO CLIENTE (INJECTED DATA)
==================================================
Dados Cadastrais e Perfil:
- Cliente: João Silva (32 anos, Analista de Sistemas)
- Perfil de Investimento: Moderado (Aceita risco: Não)
- Renda Mensal Declarada: R$ 5.000,00
- Patrimônio Total: R$ 15.000,00

Metas Financeiras Atuais:
1. Completar reserva de emergência: Necessário R$ 15.000,00 | Atual: R$ 10.000,00 (Progresso: 66.6%) | Prazo: 2026-06
2. Entrada do apartamento: Necessário R$ 50.000,00 | Prazo: 2027-12

Resumo do Fluxo de Caixa Recente (Outubro/2025):
- Saldo Inicial (Receitas): R$ 5.000,00
- Total de Despesas (Saídas): R$ 2.538,90
- Saldo Disponível para Investimento: R$ 2.461,10

Últimas Transações Registradas:
- 2025-10-15: Conta de Luz (moradia) - R$ 180.00 (saida)
- 2025-10-20: Academia (saude) - R$ 99.00 (saida)
- 2025-10-25: Combustível (transporte) - R$ 250.00 (saida)

Histórico de Interações Relevantes:
- 2025-10-01 (Chat - Tema: Tesouro Selic): Cliente pediu explicação sobre o funcionamento do Tesouro Direto.
- 2025-10-12 (Chat - Tema: Metas financeiras): Cliente acompanhou o progresso da reserva de emergência.

Produtos Financeiros Disponíveis para Recomendação:
- Tesouro Selic (Renda Fixa | Risco: Baixo | Rentabilidade: 100% da Selic | Aporte Mín: R$ 30,00)
- CDB Liquidez Diária (Renda Fixa | Risco: Baixo | Rentabilidade: 102% do CDI | Aporte Mín: R$ 100,00)
==================================================
