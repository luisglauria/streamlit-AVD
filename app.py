# [IA] Claude – esqueleto do app.py (sidebar, widgets mínimos e colunas), sem a Skill do Streamlit
# [IA] Claude – Aula 22: sintaxe de cache, heatmap (seaborn), histogramas e tabs; tratamento de 0/1 variável
# [IA] Claude – Aula 22: sintaxe do Dashboard 2 (st.metric, groupby e gráfico Altair); métricas e recorte escolhidos por mim
from pathlib import Path

import matplotlib.pyplot as plt
import altair as alt
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


# [IA] Claude – Aula 22: carregamento com @st.cache_data
@st.cache_data
def carregar_dados():
    return pd.read_csv(CAMINHO_DADOS)


df = carregar_dados()

# Faixas operacionais de frequência (cortes definidos por mim para facilitar a leitura da coordenação)
df["faixa_freq"] = pd.cut(
    df["attendance_percent"],
    bins=[0, 75, 90, 100],
    labels=["Baixa", "Média", "Alta"],
    include_lowest=True,
)

st.title("Desempenho Estudantil")
tab1, tab2 = st.tabs(["Dashboard 1: Correlação e Distribuição", "Dashboard 2: KPIs"])

# ---------------- Dashboard 1 ----------------
with tab1:
    # --- Sidebar: filtros ---
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

    # Aplica o filtro de intervalo e recalcula tudo a partir dele
    df_f = df[df["final_exam_score"].between(intervalo[0], intervalo[1])]
    st.caption(f"{len(df_f)} de {len(df)} alunos no intervalo selecionado.")

    col_corr, col_dist = st.columns([1, 1.5])

    # --- Correlação ---
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

    # --- Distribuição ---
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

# ---------------- Dashboard 2 ----------------
with tab2:
    st.subheader("KPIs de desempenho")
    st.caption("Calculados sobre todos os alunos (não dependem dos filtros do Dashboard 1).")

    media_nota = df["final_exam_score"].mean()
    media_estudo = df["study_time_hours"].mean()
    variacao = (df["final_exam_score"] - df["previous_grade"]).mean()

    k1, k2, k3 = st.columns(3)
    k1.metric("Média da nota final", f"{media_nota:.1f}")
    k2.metric("Média de horas de estudo (por dia)", f"{media_estudo:.2f} h")
    k3.metric("Variação média (nota final − nota anterior)", f"{variacao:+.1f} pontos")

    st.subheader("Desempenho Alto por faixa de frequência")
    tabela = (
        df.assign(alto=df["situacao"] == "Desempenho Alto")
        .groupby("faixa_freq", observed=True)["alto"]
        .agg(proporcao="mean", n="size")
        .reset_index()
    )
    tabela["rotulo"] = tabela.apply(
        lambda r: f"{r['proporcao']:.1%} (n={int(r['n'])})", axis=1
    )

    barras = alt.Chart(tabela).mark_bar(color=COR_DESTAQUE).encode(
        x=alt.X("faixa_freq:N", title="Faixa de frequência", sort=["Baixa", "Média", "Alta"]),
        y=alt.Y("proporcao:Q", title="Proporção de Desempenho Alto",
                scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format="%")),
        tooltip=["faixa_freq", alt.Tooltip("proporcao:Q", format=".1%"), "n"],
    )
    textos = barras.mark_text(dy=-8, color=COR_DESTAQUE).encode(text="rotulo:N")
    st.altair_chart(\n        barras + textos,\n        width="stretch",\n        alt="Proporção de Desempenho Alto por faixa de frequência.",\n    )\n    st.caption(\n        "Faixas operacionais: Baixa até 75%, Média de 75% a 90%, Alta acima de 90%. "\n        "O gráfico mostra uma associação descritiva, não uma relação de causa."\n    )\n\n    col_notas, col_estudo = st.columns(2)\n\n    with col_notas:\n        st.subheader("Distribuição das notas finais")\n        notas = (\n            alt.Chart(df)\n            .mark_bar(color=COR_DESTAQUE)\n            .encode(\n                x=alt.X("final_exam_score:Q", bin=alt.Bin(maxbins=12), title="Nota final"),\n                y=alt.Y("count():Q", title="Quantidade de alunos"),\n                tooltip=[alt.Tooltip("count():Q", title="Alunos")],\n            )\n        )\n        st.altair_chart(notas, width="stretch", alt="Distribuição das notas finais dos alunos.")\n\n    with col_estudo:\n        st.subheader("Horas de estudo e nota final")\n        pontos = (\n            alt.Chart(df)\n            .mark_circle(size=65, opacity=0.55)\n            .encode(\n                x=alt.X("study_time_hours:Q", title="Horas de estudo por dia"),\n                y=alt.Y("final_exam_score:Q", title="Nota final"),\n                color=alt.Color("situacao:N", title="Situação"),\n                tooltip=["study_time_hours:Q", "final_exam_score:Q", "situacao:N"],\n            )\n        )\n        tendencia = (\n            alt.Chart(df)\n            .transform_regression("study_time_hours", "final_exam_score")\n            .mark_line(color="#b85c5c", size=2)\n            .encode(x=alt.X("study_time_hours:Q"), y=alt.Y("final_exam_score:Q"))\n        )\n        st.altair_chart(pontos + tendencia, width="stretch", alt="Relação entre horas de estudo por dia e nota final.")