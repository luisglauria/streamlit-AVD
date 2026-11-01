# [IA] Claude – esqueleto do app.py (sidebar, widgets mínimos e colunas), sem a Skill do Streamlit
# [IA] Claude – Aula 22: sintaxe de cache, heatmap (seaborn)
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Desempenho Estudantil", layout="wide")

CAMINHO_DADOS = Path(__file__).parent / "data" / "clean" / "dataset.csv"
VARS_QUANT = [
    "study_time_hours",
    "attendance_percent",
    "sleep_hours",
    "previous_grade",
    "final_exam_score",
]
COR_DESTAQUE = "#2d223a"
COR_CONTEXTO = "#e9d4d0"

@st.cache_data
def carregar_dados():
    return pd.read_csv(CAMINHO_DADOS)


df = carregar_dados()

st.title("Desempenho Estudantil")
tab1, tab2 = st.tabs(["Dashboard 1: Correlação e Distribuição", "Dashboard 2: KPIs"])

with tab1:

    with st.sidebar:
        st.header("Filtros")
        variaveis = st.multiselect(
            "Variáveis quantitativas",
            options=VARS_QUANT,
            default=VARS_QUANT,
        )
        nota_min = float(df["final_exam_score"].min())
        nota_max = float(df["final_exam_score"].max())
        intervalo = st.slider(
            "Intervalo da nota final",
            min_value=nota_min,
            max_value=nota_max,
            value=(nota_min, nota_max),
        )

    df_f = df[df["final_exam_score"].between(intervalo[0], intervalo[1])]
    st.caption(f"{len(df_f)} de {len(df)} alunos no intervalo selecionado.")

    col_corr, col_dist = st.columns([1, 1.5])

    with col_corr:
        st.subheader("Correlação (Spearman)")
        if len(variaveis) < 2:
            st.info("Selecione ao menos 2 variáveis para ver a correlação.")
        elif len(df_f) < 3:
            st.warning("Poucos alunos no intervalo escolhido para calcular a correlação.")
        else:
            corr = df_f[variaveis].corr(method="spearman")
            fig, ax = plt.subplots(figsize=(5, 4.5))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                        vmin=-1, vmax=1, square=True, ax=ax)
            ax.tick_params(axis="x", rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

    with col_dist:
        st.subheader("Distribuição")
        if len(variaveis) == 0:
            st.info("Selecione ao menos 1 variável para ver a distribuição.")
        elif len(df_f) == 0:
            st.warning("Nenhum aluno no intervalo escolhido.")
        else:
            n_cols = 2
            n_linhas = -(-len(variaveis) // n_cols)
            fig, axes = plt.subplots(n_linhas, n_cols, figsize=(8, 3 * n_linhas),
                                     squeeze=False)
            axes = axes.ravel()
            for ax, col in zip(axes, variaveis):
                sns.histplot(data=df_f, x=col, kde=True, color=COR_DESTAQUE, ax=ax)
                ax.set_title(col)
                ax.set_ylabel("")
            for ax in axes[len(variaveis):]:
                ax.axis("off")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

with tab2:
    st.subheader("KPIs")
    st.info("Em construção: as métricas serão definidas por você e justificadas em "
            "entregas/justificativa-metricas.md.")