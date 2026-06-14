import json
import os
import google.generativeai as genai
import pandas as pd
import requests
import streamlit as st

# ==================================================
# 1. CONFIGURAÇÕES DA API (Escolha uma das opções)
# ==================================================

# OPÇÃO A: Google Gemini (Recomendado - Gratuito e em nuvem)
# Substitua pelo seu token obtido no Google AI Studio
API_KEY_GEMINI = "SUA_CHAVE_GEMINI_AQUI"
genai.configure(api_key=API_KEY_GEMINI)

# OPÇÃO B: Ollama Local (Se preferir rodar o Llama 3 offline)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO_OLLAMA = "llama3"


# ==================================================
# 2. CARREGAR BASE DE CONHECIMENTO (DATA)
# ==================================================
@st.cache_data
def carregar_dados():
    perfil_json = json.load(open("../data/perfil_investidor.json", encoding="utf-8"))
    produtos_json = json.load(
        open("../data/produtos_financeiros.json", encoding="utf-8")
    )
    transacoes_df = pd.read_csv("../data/transacoes.csv")
    historico_df = pd.read_csv("../data/historico_atendimento.csv")
    return perfil_json, produtos_json, transacoes_df, historico_df


perfil, produtos, transacoes, historico = carregar_dados()


# ==================================================
# 3. CÁLCULOS E MONTAGEM DO CONTEXTO (ANTI-ALUCINAÇÃO)
# ==================================================
# Computação prévia de valores exatos via Pandas para blindar a LLM contra erros matemáticos
total_receitas = transacoes[transacoes["tipo"] == "entrada"]["valor"].sum()
total_despesas = transacoes[transacoes["tipo"] == "saida"]["valor"].sum()
saldo_livre = total_receitas - total_despesas

contexto = f"""
==================================================
CONTEXTO DO CLIENTE (INJECTED DATA)
==================================================
Dados Cadastrais e Perfil:
- Cliente: {perfil['nome']} ({perfil['idade']} anos, {perfil['profissao']})
- Perfil de Investimento: {perfil['perfil_investidor']} (Aceita risco: {perfil['aceita_risco']})
- Renda Mensal Declarada: R$ {perfil['renda_mensal']:.2f}
- Patrimônio Total: R$ {perfil['patrimonio_total']:.2f}

Metas Financeiras Atuais:
1. {perfil['metas'][0]['meta']}: Necessário R$ {perfil['metas'][0]['valor_necessario']:.2f} | Atual: R$ {perfil['reserva_emergencia_atual']:.2f} | Prazo: {perfil['metas'][0]['prazo']}
2. {perfil['metas'][1]['meta']}: Necessário R$ {perfil['metas'][1]['valor_necessario']:.2f} | Prazo: {perfil['metas'][1]['prazo']}

Resumo do Fluxo de Caixa Recente Calculado (Outubro/2025):
- Saldo Inicial (Receitas): R$ {total_receitas:.2f}
- Total de Despesas (Saídas): R$ {total_despesas:.2f}
- Saldo Disponível para Investimento: R$ {saldo_livre:.2f}

Últimas Transações Registradas (Extrato Bruto):
{transacoes.to_string(index=False)}

Histórico de Interações Anteriores:
{historico.to_string(index=False)}

Produtos Financeiros Disponíveis para Recomendação:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
==================================================
"""


# ==================================================
# 4. SYSTEM PROMPT (PROPRIEDADES DA PERSONA)
# ==================================================
SYSTEM_PROMPT = """Você é o Breno, um agente financeiro inteligente, consultivo e proativo, especializado em finanças pessoais para o cliente João Silva.

OBJETIVO:
Guiar o usuário na conclusão de sua Reserva de Emergência e no planejamento de metas de forma educativa, antecipando necessidades.

REGRAS DE OURO:
1. Fonte Única da Verdade: Baseie suas respostas estritamente no bloco de dados fornecido no contexto. Nunca invente saldos, despesas ou produtos.
2. Tratamento de Dados Ausentes: Se o usuário perguntar por uma transação ou investimento inexistente no contexto, diga explicitamente: "Não localizei esse registro no seu histórico atual, mas posso simular se você me passar o valor."
3. Proatividade Estratégica: Sempre que o cliente perguntar sobre seu saldo ou metas, mostre o cálculo do saldo livre calculado (R$ 2.461,10) e sugira ativamente um aporte direcionado para o Tesouro Selic ou CDB Liquidez Diária para atingir os R$ 15.000,00 da Reserva.
4. Restrição de Recomendações: Você está proibido de sugerir ações ou fundos de ações de alto risco para a meta atual. Recomende apenas os ativos de baixo risco listados.
5. Tom de Voz: Acessível, direto e encorajador. Responda de forma sucinta em até 3 parágrafos.
"""


# ==================================================
# 5. INTEGRAÇÃO COM MODELOS DE IA
# ==================================================
def chamar_gemini(mensagem_usuario):
    """Executa a chamada ao modelo Gemini do Google"""
    prompt_final = f"{SYSTEM_PROMPT}\n\n{contexto}\n\nUsuário: {mensagem_usuario}\nBreno:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt_final)
    return response.text


def chamar_ollama_local(mensagem_usuario):
    """Função alternativa para rodar o Llama 3 localmente via Ollama"""
    prompt_final = f"{SYSTEM_PROMPT}\n\n{contexto}\n\nUsuário: {mensagem_usuario}\nBreno:"
    payload = {"model": MODELO_OLLAMA, "prompt": prompt_final, "stream": False}
    r = requests.post(OLLAMA_URL, json=payload)
    return r.json()["response"]


# Escolha qual motor de IA você deseja ativar para o chat:
def perguntar_ao_agente(msg):
    return chamar_gemini(msg)  # Altere para chamar_ollama_local(msg) se rodar local


# ==================================================
# 6. INTERFACE DE USUÁRIO (STREAMLIT)
# ==================================================
st.set_page_config(page_title="Breno - Agente Financeiro", page_icon="💰")
st.title("💰 Breno, seu Agente Financeiro")
st.markdown(
    "Pergunte-me sobre seu saldo livre, análise de gastos ou simulação de metas."
)

# Inicializa o histórico do chat se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Renderiza mensagens anteriores do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura nova interação do usuário
if pergunta := st.chat_input("Digite sua dúvida financeira aqui..."):
    # Mostra e guarda mensagem do usuário
    st.chat_message("user").markdown(pergunta)
    st.session_state.messages.append({"role": "user", "content": pergunta})

    # Gera e exibe resposta do agente
    with st.spinner("Analisando sua base de dados..."):
        resposta_agente = perguntar_ao_agente(pergunta)

    st.chat_message("assistant").markdown(resposta_agente)
    st.session_state.messages.append(
        {"role": "assistant", "content": resposta_agente}
    )
