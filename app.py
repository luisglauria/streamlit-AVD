# [IA] Claude – esqueleto do app.py (sidebar com widgets mínimos e colunas com placeholders), sem a Skill do Streamlit
import streamlit as st

st.set_page_config(page_title="Desempenho Estudantil", layout="wide")

VARS_QUANT = [
    "study_time_hours",
    "attendance_percent",
    "sleep_hours",
    "previous_grade",
    "final_exam_score",
]

st.title("Dashboard 1: Correlação e Distribuição")

# --- Sidebar: filtros ---
with st.sidebar:
    st.header("Filtros")
    variaveis = st.multiselect(
        "Variáveis quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
    )
    intervalo = st.slider(
        "Intervalo da nota final",
        min_value=0,
        max_value=100,
        value=(0, 100),
    )

# --- Área principal ---
col_corr, col_dist = st.columns(2)

with col_corr:
    st.subheader("Correlação")
    st.info("Placeholder: heatmap de correlação")

with col_dist:
    st.subheader("Distribuição")
    st.info("Placeholder: histogramas")

st.caption(f"Variáveis: {variaveis} | Intervalo: {intervalo}")
