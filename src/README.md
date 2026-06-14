# Código da Aplicação

Esta seção apresenta o protótipo funcional do agente financeiro desenvolvido em Python, integrando a interface em Streamlit à API de inteligência artificial.

## Estrutura do Projeto

```text
src/
├── app.py              # Aplicação principal unificada (Streamlit + IA)
└── requirements.txt    # Dependências do projeto
```
## Dependências (requirements.txt)
```
streamlit
google-generativeai
pandas
```

## Código da Aplicação (src/app.py)
O código abaixo carrega a base de conhecimento (arquivos JSON e CSV do cliente João Silva), monta o contexto dinâmico de forma estruturada e gerencia a conversa utilizando a API do Gemini.

(Caso prefira usar o Ollama local, basta descomentar a função alternativa indicada no código).

## Código Completo
Todo o código-fonte está no arquivo app.py.

## Como Executar a Aplicação
Siga os comandos abaixo no seu terminal para colocar o agente em funcionamento:
```
# 1. Navegar até a pasta do código do projeto
cd src

# 2. Instalar as dependências leves necessárias
pip install -r requirements.txt

# 3. Iniciar o servidor local da aplicação Streamlit
streamlit run app.py
```
