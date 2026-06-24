# StudyAgent — Agente Organizador de Estudos com LLM

Projeto acadêmico que demonstra o uso de um **agente baseado em LLM** para gerar planos de estudo personalizados de forma automática.

---

## O que é?

O **StudyAgent** é um agente inteligente que recebe informações do estudante (matéria, prazo, horas disponíveis, nível de dificuldade e objetivo) e, utilizando um **Modelo de Linguagem (LLM)** via Ollama, monta automaticamente um cronograma de estudos completo com:

- Distribuição de conteúdo por dias  
- Sessões de estudo com pausas  
- Dicas de técnicas de aprendizagem  
- Mensagem motivacional personalizada  
- Exportação em PDF  
- Histórico de planos gerados  

---

## Estrutura do Projeto

```
study-agent/
├── app.py               ← Interface Streamlit (tela principal)
├── llm/
│   ├── __init__.py
│   └── planner.py       ← Agente LLM (StudyPlannerAgent)
├── utils/
│   ├── __init__.py
│   └── helpers.py       ← Exportação PDF, histórico, formatação
├── data/
│   └── history.json     ← Histórico de planos (gerado automaticamente)
├── requirements.txt
├── .env                 ← Credenciais (não versionar!)
└── README.md
```

---

## Como Executar

### 1. Clone ou baixe o projeto

```bash
cd study-agent
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o `.env`

Abra o arquivo `.env` e preencha com suas credenciais:

```env
OLLAMA_API_KEY=sua_chave_aqui
OLLAMA_HOST=https://ollama.com
OLLAMA_MODEL=llama3.2
```

> **Onde obter a API Key?** Acesse [ollama.com/settings/keys](https://ollama.com/settings/keys) e gere uma chave.

### 5. Execute o projeto

```bash
streamlit run app.py
```

Acesse em: **http://localhost:8501**

---

## Uso Offline (sem API Key)

Caso não tenha uma chave de API, o sistema opera em **modo local** com um planejador pedagógico embutido. O plano gerado seguirá as mesmas regras (Pomodoro, pausas, revisão final), porém sem personalização via LLM.

Isso permite **demonstração completa do projeto** mesmo sem conexão à internet.

---

## Arquitetura do Agente

```
Usuário
  │
  ▼
Formulário Streamlit (app.py)
  │  nome, matéria, prazo, horas, dificuldade, objetivo
  ▼
StudyPlannerAgent (llm/planner.py)
  │  monta system_prompt + user_prompt
  ▼
Ollama LLM (llama3.2 / cloud ou local)
  │  responde em JSON estruturado
  ▼
Exibição do Plano (app.py)
  │  cronograma, dicas, mensagem motivacional
  ▼
Exportação PDF + Histórico (utils/helpers.py)
```

---

## Dependências

| Pacote | Uso |
|---|---|
| `streamlit` | Interface web |
| `ollama` | Cliente LLM (Ollama Cloud ou local) |
| `fpdf2` | Exportação de PDF |
| `python-dotenv` | Leitura do `.env` |


## Observações Acadêmicas

- O uso do LLM é explicitamente indicado na interface com o badge **"🤖 Gerado por LLM"**
- O fallback para o modo local garante que a demonstração funcione mesmo sem conexão
- O prompt do agente segue princípios de psicopedagogia (Pomodoro, Feynman, repetição espaçada)
- Todo o código é comentado para facilitar a compreensão acadêmica
