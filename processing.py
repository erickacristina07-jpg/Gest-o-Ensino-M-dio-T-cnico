"""Limpeza de dados e métricas agregadas do dashboard."""
import pandas as pd

# Categorias baseadas na estrutura da planilha GESTÃO DE DADOS 2026.xlsx.
INDICATORS = [
    "Clubes", "NOA", "NPS", "Evasão", "Atendimentos psicopedagógicos",
    "Rendimento", "Geekie - estudantes", "Geekie - docentes", "Ocorrências",
    "Inclusão / PEI", "Formações", "Olimpíadas"
]
CATEGORIES = [
    "Matemática", "Português", "Física", "Química", "Linguagens", "Humanas",
    "Matemática e suas Tecnologias", "Natureza", "Geral", "Desafiar", "Orientar",
    "Intervir", "Atividades enviadas", "Corrigidas", "Alunos aprovados",
    "Alunos retidos", "Participação", "Outro"
]
CAMPI = ["Zona Norte", "Mossoró", "Outro"]
SERIES = ["1ª Série A", "1ª Série B", "2ª Série A", "2ª Série B", "3ª Série A", "3ª Série B"]
STATUSES = ["Registrado", "Em acompanhamento", "Concluído", "Atenção", "Não se aplica"]

def clean_records(records):
    """Padroniza strings, datas e valores sem alterar a origem armazenada."""
    if records is None or len(records) == 0:
        return pd.DataFrame(columns=["id","record_date","campus","indicator","category","series","status","value","unit","source","notes","created_at"])
    df = pd.DataFrame(records)
    for col in ["campus", "indicator", "category", "series", "status", "unit", "source", "notes"]:
        if col in df:
            df[col] = df[col].fillna("").astype(str).str.strip()
    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    df = df.dropna(subset=["record_date"])
    return df

def calculate_kpis(df):
    if df.empty:
        return {"records": 0, "campuses": 0, "indicators": 0, "sum_value": 0.0, "mean_value": 0.0}
    return {
        "records": int(len(df)),
        "campuses": int(df["campus"].nunique()),
        "indicators": int(df["indicator"].nunique()),
        "sum_value": float(df["value"].sum()),
        "mean_value": float(df["value"].mean()),
    }
