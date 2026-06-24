import os
import json
from datetime import datetime, timedelta
from groq import Groq
import streamlit as st


class StudyPlannerAgent:

    def __init__(self, api_key=None, model=None):

        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        self.client = None

        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                st.error(f"Erro criando cliente Groq: {e}")

    def is_configured(self):
        return self.client is not None and bool(self.api_key) and bool(self.model)

    def generate_study_plan(
        self,
        student_name,
        subject,
        target_date,
        daily_hours,
        difficulty,
        goal,
        extra_info=""
    ):

        today = datetime.now().date()

        if isinstance(target_date, str):
            target_date = datetime.strptime(
                target_date,
                "%Y-%m-%d"
            ).date()

        days_available = max(
            1,
            (target_date - today).days
        )

        student_name = (
            student_name
            if student_name
            else "Estudante"
        )

        if not self.is_configured():
            raise Exception(
                "Groq não configurado corretamente. "
                "Defina GROQ_API_KEY no arquivo .env"
            )

        system_prompt = """
Você é um organizador de estudos especialista em criar planos de estudo personalizados.

Gere UM plano de estudo completo seguindo EXATAMENTE esta estrutura JSON. NÃO adicione campos extras.

REGRAS:
- total_days: número de dias entre hoje e a data da prova
- daily_hours: horas de estudo por dia
- Cada dia em daily_plan deve ter: day (numero), date (formato "YYYY-MM-DD"), focus (tema do dia), sessions (lista de sessoes)
- Cada sessão deve ter: topic, duration_minutes, description, is_break (false para estudo, true para pausa)
- Inclua pausas curtas entre sessoes de estudo
- Distribua o conteudo de forma progressiva (facil -> dificil)

ESTRUTURA EXATA:
{
  "student_name": "Maria Silva",
  "subject": "Calculo I",
  "total_days": 14,
  "daily_hours": 2,
  "motivational_message": "Voce e capaz! Com dedicação diaria, vai chegar la!",
  "general_recommendations": [
    "Revise o conteudo do dia anterior antes de comecar",
    "Resolva exercicios de provas anteriores",
    "Durma bem para fixar o conteudo"
  ],
  "daily_plan": [
    {
      "day": 1,
      "date": "2026-06-15",
      "focus": "Introducao e conceitos basicos",
      "sessions": [
        {"topic": "Revisao de fundamentos", "duration_minutes": 45, "description": "Revisar algebra basica e trigonometria essencial", "is_break": false},
        {"topic": "Pausa", "duration_minutes": 10, "description": "Pausa para descanso", "is_break": true},
        {"topic": "Limites", "duration_minutes": 50, "description": "Estudo de limites e suas propriedades", "is_break": false}
      ]
    }
  ]
}
"""

        user_prompt = f"""
Aluno: {student_name}

Matéria:
{subject}

Dias:
{days_available}

Horas:
{daily_hours}

Dificuldade:
{difficulty}

Objetivo:
{goal}

Extras:
{extra_info}
"""

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )

            content = response.choices[0].message.content

            data = json.loads(content)

            # Ensure daily_plan has the expected structure
            if "daily_plan" in data and isinstance(data["daily_plan"], list):
                for day_entry in data["daily_plan"]:
                    # Fix missing keys
                    if "day" not in day_entry:
                        day_entry["day"] = data["daily_plan"].index(day_entry) + 1
                    if "date" not in day_entry:
                        day_entry["date"] = (today + timedelta(days=day_entry["day"] - 1)).strftime("%Y-%m-%d")
                    if "focus" not in day_entry:
                        day_entry["focus"] = "Estudo diario"
                    if "sessions" not in day_entry or not isinstance(day_entry["sessions"], list):
                        day_entry["sessions"] = []

            data["is_simulated"] = False

            return data

        except Exception as e:

            st.error("Erro REAL do LLM (Groq)")
            st.code(str(e))

            raise
