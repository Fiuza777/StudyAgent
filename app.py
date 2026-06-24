"""
StudyAgent – Agente Organizador de Estudos
Interface principal Streamlit
"""
import streamlit as st
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

# ── Carrega variáveis do .env ────────────────────────────────────────────────
load_dotenv()

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="StudyAgent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports internos ──────────────────────────────────────────────────────────
from llm.planner import StudyPlannerAgent
from utils.helpers import (
    save_plan_to_history, load_history, clear_history,
    export_plan_to_pdf, format_duration, total_study_minutes,
)

# ── CSS personalizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Importa fontes */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

/* Reset geral */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Fundo principal */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    min-height: 100vh;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid rgba(99,102,241,0.3);
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Título Hero */
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #c084fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
    line-height: 1.1;
}
.hero-sub {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-top: 6px;
    margin-bottom: 28px;
}

/* Cards */
.card {
    background: rgba(30, 27, 75, 0.6);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    backdrop-filter: blur(10px);
}
.card-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #818cf8;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Badge LLM / Mock */
.badge-llm {
    display: inline-block;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-mock {
    display: inline-block;
    background: rgba(100,116,139,0.4);
    color: #94a3b8;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border: 1px solid rgba(100,116,139,0.4);
}

/* Motivacional */
.motivacional {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(192,132,252,0.15));
    border-left: 4px solid #818cf8;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    color: #c7d2fe;
    font-size: 1rem;
    font-style: italic;
    margin: 16px 0;
}

/* Sessão de estudo */
.session-study {
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px;
    padding: 12px 16px;
    margin: 6px 0;
    color: #e2e8f0;
}
.session-break {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 10px;
    padding: 10px 16px;
    margin: 6px 0;
    color: #6ee7b7;
    font-size: 0.9rem;
}

/* Estatísticas */
.stat-box {
    background: rgba(30,27,75,0.8);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #818cf8;
}
.stat-label {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 2px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Rec item */
.rec-item {
    background: rgba(30,27,75,0.5);
    border-radius: 8px;
    padding: 10px 14px;
    color: #cbd5e1;
    margin: 6px 0;
    font-size: 0.92rem;
    border-left: 3px solid #6366f1;
}

/* Botão primário override */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 10px 28px !important;
    width: 100%;
    transition: opacity 0.2s;
}
.stButton > button:hover {
    opacity: 0.88 !important;
}

/* Inputs */
.stTextInput input, .stSelectbox select, .stDateInput input,
.stNumberInput input, .stTextArea textarea {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* Esconder watermark Streamlit */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Estado da sessão ──────────────────────────────────────────────────────────
if "plan" not in st.session_state:
    st.session_state.plan = None
if "generating" not in st.session_state:
    st.session_state.generating = False
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "planner"


# ── Sidebar: configurações ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuração do Agente")
    st.markdown("---")

    st.markdown("### 🔗 Conexão Groq")
    st.caption("Configuração carregada automaticamente do arquivo .env")

    # Usa somente as variáveis do .env
    agent = StudyPlannerAgent()

    # Apenas para exibir no layout
    groq_model = agent.model

    st.markdown("---")
    # Não validar conexão aqui
    st.success(f"🤖 Modelo carregado: {agent.model}")
    st.markdown(
    '<span class="badge-llm">🤖 Modo LLM Ativo</span>',
    unsafe_allow_html=True
)

    st.markdown("---")
    st.markdown("### 📖 Sobre o Projeto")
    st.caption("**StudyAgent** é um agente baseado em LLM que gera planos de estudo personalizados.")
    st.caption("Desenvolvido com Python + Streamlit + Groq.")

    st.markdown("---")
    if st.button("🗑️ Limpar Histórico"):
        clear_history()
        st.success("Histórico apagado!")


# ── Conteúdo principal ────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">📚 StudyAgent</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Agente Inteligente de Planejamento de Estudos com LLM</p>', unsafe_allow_html=True)

tab_planner, tab_history = st.tabs(["🎯 Novo Plano", "📋 Histórico"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 – FORMULÁRIO + RESULTADO
# ════════════════════════════════════════════════════════════════════════════
with tab_planner:

    col_form, col_result = st.columns([1, 1.4], gap="large")

    # ── Formulário ──────────────────────────────────────────────────────────
    with col_form:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📝 Dados do Estudante</div>', unsafe_allow_html=True)

        student_name = st.text_input("Nome do aluno (opcional)", placeholder="Ex: Maria Silva")
        subject = st.text_input("Disciplina / Matéria *", placeholder="Ex: Cálculo I, Direito Penal...")

        col_date, col_hours = st.columns(2)
        with col_date:
            min_date = date.today() + timedelta(days=1)
            target_date = st.date_input(
                "Data da prova *",
                value=date.today() + timedelta(days=14),
                min_value=min_date,
                format="DD/MM/YYYY",
            )
        with col_hours:
            daily_hours = st.number_input(
                "Horas por dia *", min_value=1, max_value=12, value=2, step=1
            )

        difficulty = st.select_slider(
            "Nível de dificuldade",
            options=["Fácil", "Médio", "Difícil"],
            value="Médio",
        )

        goal = st.selectbox(
            "Objetivo *",
            ["Passar na prova", "Tirar nota alta", "Revisar conteúdo",
             "Aprender do zero", "Reforçar pontos fracos"],
        )

        extra_info = st.text_area(
            "Tópicos ou conteúdos específicos (opcional)",
            placeholder="Ex: Derivadas, Integrais, Limites (separados por vírgula)",
            height=90,
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Botão de geração
        gerar = st.button("🚀 Gerar Plano de Estudos", use_container_width=True)

        # LLM indicator
        if agent.is_configured():
            st.markdown(
                f'<div style="text-align:center;margin-top:8px;">'
                f'<span class="badge-llm">🤖 Usando LLM: {groq_model}</span></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="text-align:center;margin-top:8px;">'
                '<span class="badge-mock">📋 Planejador Local</span></div>',
                unsafe_allow_html=True
            )

    # ── Geração ──────────────────────────────────────────────────────────────
    if gerar:
        if not subject:
            st.error("⚠️ Preencha a matéria antes de gerar o plano.")
        else:
            with col_result:
                with st.spinner("🧠 O agente está montando seu plano personalizado..."):
                    progress = st.progress(0, text="Conectando ao agente...")
                    import time
                    for i in range(1, 5):
                        time.sleep(0.3)
                        progress.progress(i * 20, text=f"Processando... {i*20}%")

                    plan = agent.generate_study_plan(
                        student_name=student_name,
                        subject=subject,
                        target_date=target_date,
                        daily_hours=daily_hours,
                        difficulty=difficulty,
                        goal=goal,
                        extra_info=extra_info,
                    )
                    progress.progress(100, text="Plano gerado! ✅")
                    time.sleep(0.4)
                    progress.empty()

                st.session_state.plan = plan
                save_plan_to_history(plan)

    # ── Resultado ────────────────────────────────────────────────────────────
    with col_result:
        plan = st.session_state.plan

        if plan is None:
            st.markdown("""
            <div class="card" style="text-align:center; padding: 48px 24px; color:#475569;">
                <div style="font-size:3.5rem; margin-bottom:12px;">🎓</div>
                <div style="font-size:1.1rem; color:#64748b;">
                    Preencha o formulário ao lado e clique em<br>
                    <strong style="color:#818cf8;">Gerar Plano de Estudos</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Badge de origem
            if plan.get("is_simulated"):
                st.markdown('<span class="badge-mock">📋 Gerado pelo Planejador Local</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="badge-llm">🤖 Gerado por LLM — {groq_model}</span>', unsafe_allow_html=True)

            # Mensagem motivacional
            st.markdown(
                f'<div class="motivacional">✨ {plan.get("motivational_message", "")}</div>',
                unsafe_allow_html=True,
            )

            # Estatísticas
            total_study = total_study_minutes(plan)
            days = plan.get("total_days", 0)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="stat-box"><div class="stat-value">{days}</div><div class="stat-label">Dias de Estudo</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="stat-box"><div class="stat-value">{plan.get("daily_hours",0)}h</div><div class="stat-label">Por Dia</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="stat-box"><div class="stat-value">{format_duration(total_study)}</div><div class="stat-label">Total de Estudo</div></div>', unsafe_allow_html=True)

            st.markdown("---")

            # Barra de progresso do plano
            total_days = plan.get("total_days", 1)
            days_done = 0  # simulação — pode ser expandido
            st.markdown(f"**📅 Progresso do Plano** — {days_done}/{total_days} dias concluídos")
            st.progress(days_done / total_days if total_days else 0)

            # Recomendações
            st.markdown("#### 💡 Recomendações de Estudo")
            for rec in plan.get("general_recommendations", []):
                st.markdown(f'<div class="rec-item">• {rec}</div>', unsafe_allow_html=True)

            st.markdown("---")

            # Cronograma diário
            st.markdown("#### 📅 Cronograma Diário")
            for day in plan.get("daily_plan", []):
                with st.expander(
                    f"📆 Dia {day['day']} — {day['date']}  |  {day['focus']}",
                    expanded=(day["day"] == 1),
                ):
                    for s in day.get("sessions", []):
                        if s.get("is_break"):
                            st.markdown(
                                f'<div class="session-break">☕ <strong>{s["topic"]}</strong> '
                                f'({s["duration_minutes"]} min)<br>'
                                f'<span style="font-size:0.85rem">{s["description"]}</span></div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<div class="session-study">📖 <strong>{s["topic"]}</strong> '
                                f'({s["duration_minutes"]} min)<br>'
                                f'<span style="font-size:0.85rem;color:#94a3b8">{s["description"]}</span></div>',
                                unsafe_allow_html=True,
                            )

            # Exportar PDF
            st.markdown("---")
            col_pdf, col_new = st.columns(2)
            with col_pdf:
                try:
                    pdf_bytes = export_plan_to_pdf(plan)
                    st.download_button(
                        label="⬇️ Exportar PDF",
                        data=pdf_bytes,
                        file_name=f"plano_{plan.get('subject','estudo').lower().replace(' ','_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except ImportError:
                    st.info("📎 Para exportar PDF instale: `pip install fpdf2`")
            with col_new:
                if st.button("🔄 Novo Plano", use_container_width=True):
                    st.session_state.plan = None
                    st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 – HISTÓRICO
# ════════════════════════════════════════════════════════════════════════════
with tab_history:
    history = load_history()

    if not history:
        st.markdown("""
        <div class="card" style="text-align:center; padding: 40px; color:#475569;">
            <div style="font-size:2.5rem;">📭</div>
            <div style="margin-top:8px; color:#64748b;">Nenhum plano gerado ainda.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"### 📋 {len(history)} plano(s) gerado(s)")
        for entry in reversed(history):
            with st.expander(
                f"#{entry['id']} — {entry['subject']}  |  {entry['student_name']}  |  {entry['created_at']}"
            ):
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Dias", entry["total_days"])
                col_b.metric("Horas/dia", entry["daily_hours"])
                col_c.metric("Origem", "LLM" if not entry["is_simulated"] else "Local")

                if st.button(f"📂 Carregar plano #{entry['id']}", key=f"load_{entry['id']}"):
                    st.session_state.plan = entry["plan"]
                    st.success("Plano carregado! Veja na aba 'Novo Plano'.")
