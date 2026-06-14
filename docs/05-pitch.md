# Apresentação do Projeto (Sumário Executivo)

## Roteiro Conceitual da Solução

### 1. O Problema
O gerenciamento financeiro reativo é um dos maiores obstáculos para a saúde financeira pessoal. A maioria das pessoas monitora suas finanças apenas de forma retrospectiva, descobrindo que estourou o orçamento quando o mês já chegou ao fim. No cenário avaliado, o cliente João Silva possui uma renda estável de R$ 5.000,00 e objetivos claros, como a consolidação de uma reserva de emergência. No entanto, a falta de ferramentas proativas faz com que ele opere sem clareza sobre o seu real saldo livre diário, dificultando a constância nos aportes e o alcance de suas metas.

### 2. A Solução
Para solucionar essa dor, foi idealizado o **Breno: um Agente Financeiro Inteligente**. Diferente de chatbots tradicionais e reativos que apenas respondem a comandos, o Breno atua de forma proativa e consultiva. 

Integrando IA Generativa a um pipeline estruturado de dados em Python, o agente analisa dinamicamente o histórico de transações e as preferências do usuário. Sempre que o fluxo de caixa é consultado, a aplicação calcula previamente os valores exatos via Pandas (Receitas vs. Despesas) e o agente assume um papel ativo: ele apresenta o saldo livre real de R$ 2.461,10 e já propõe uma estratégia de alocação no Tesouro Selic, aproximando o cliente de concluir os 100% da sua meta prioritária.

### 3. Demonstração de Fluxo e Comportamento
O funcionamento lógico da aplicação unificada em Streamlit segue três pilares de interação:
* **Contextualização Inicial:** Ao iniciar o ambiente, o agente resgata o histórico de atendimentos anteriores para demonstrar memória de longo prazo, contextualizando a conversa com base em dúvidas passadas do usuário.
* **Atuação Proativa:** Diante de uma pergunta simples como *"Quanto tenho de saldo livre?"*, o backend em Python computa os dados do arquivo `transacoes.csv` e a IA formata uma resposta consultiva, incentivando o aporte imediato no CDB Liquidez Diária.
* **Segurança e Blindagem:** Diante de perguntas fora do escopo financeiro (*"Qual a previsão do tempo?"*) ou tentativas de indução a riscos inadequados (*"Quero investir em ações para enriquecer rápido"*), o agente ativa suas regras de restrição do System Prompt, recusando o desvio de forma polida e mantendo as recomendações estritamente alinhadas ao perfil moderado do cliente.

### 4. Diferencial e Impacto
O grande diferencial desta solução reside na **confiabilidade cirúrgica dos dados** e na **proatividade consultiva**. Ao realizar os cálculos matemáticos complexos diretamente no backend em Python e injetar apenas os resultados consolidados no prompt, eliminamos o risco de alucinações numéricas por parte da LLM. 

O impacto prático do projeto é a democratização do planejamento financeiro: transformamos registros estáticos de extratos bancários em um direcionamento de investimentos ativo, focado em segurança e aderente às necessidades reais do cliente.

---

## Checklist de Conformidade Textual

- [X] Problema financeiro claramente definido
- [X] Solução consultiva detalhada com cruzamento de dados
- [X] Fluxo de comportamento e tratamento de exceções demonstrado
- [X] Estratégia de segurança e barreiras anti-alucinação explicadas
- [X] Documentação final entregue no formato estrito de texto
