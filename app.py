
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

from src.data_loader import load_events, events_to_dataframe
from src.metrics import get_team_summary, get_player_summary
from src.visualizations import plot_shot_map, plot_pass_map


# =====================================================
# CONFIGURACAO
# =====================================================

st.set_page_config(
    page_title="MN Scout Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

ARQUIVO = Path("data/matches/partida_01.json")

VERDE = "#00E676"
FUNDO = "#080B09"
PAINEL = "#111713"
BORDA = "#25332A"
TEXTO = "#F2F7F3"
TEXTO_SECUNDARIO = "#98A89D"


# =====================================================
# IDENTIDADE VISUAL MN
# =====================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {{
        --mn-green: {VERDE};
        --mn-bg: {FUNDO};
        --mn-panel: {PAINEL};
        --mn-border: {BORDA};
        --mn-text: {TEXTO};
        --mn-muted: {TEXTO_SECUNDARIO};
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: var(--mn-bg);
        color: var(--mn-text);
    }}

    [data-testid="stHeader"] {{
        background: rgba(8, 11, 9, 0.95);
    }}

    [data-testid="stSidebar"] {{
        background: #0D120F;
        border-right: 1px solid var(--mn-border);
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.5rem;
    }}

    .mn-brand {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 0 22px 0;
        border-bottom: 1px solid var(--mn-border);
        margin-bottom: 28px;
    }}

    .mn-logo {{
        width: 48px;
        height: 48px;
        min-width: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--mn-green);
        color: #061009;
        border-radius: 12px;
        font-size: 25px;
        font-weight: 800;
        box-shadow: 0 0 24px rgba(0, 230, 118, 0.12);
    }}

    .mn-brand-name {{
        font-size: 19px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.7px;
        line-height: 1.2;
    }}

    .mn-brand-sub {{
        color: var(--mn-green);
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2.5px;
        margin-top: 5px;
    }}

    .mn-eyebrow {{
        color: var(--mn-green);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }}

    .mn-title {{
        font-size: clamp(28px, 4vw, 42px);
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -1.8px;
        color: #FFFFFF;
        margin: 0;
    }}

    .mn-title span {{
        color: var(--mn-green);
    }}

    .mn-description {{
        color: var(--mn-muted);
        font-size: 14px;
        line-height: 1.7;
        margin-top: 12px;
        margin-bottom: 22px;
    }}

    .mn-section {{
        color: #FFFFFF;
        font-size: 19px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 18px 0 12px 0;
    }}

    .mn-section span {{
        color: var(--mn-green);
        margin-right: 8px;
    }}

    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, #141B16, #0E130F);
        border: 1px solid var(--mn-border);
        border-radius: 14px;
        padding: 20px 20px 17px 20px;
        min-height: 125px;
    }}

    [data-testid="stMetricLabel"] {{
        color: var(--mn-muted);
        font-size: 12px;
        font-weight: 600;
    }}

    [data-testid="stMetricValue"] {{
        color: #FFFFFF;
        font-size: 32px;
        font-weight: 800;
    }}

    [data-testid="stMetricDelta"] {{
        color: var(--mn-green);
    }}

    .stButton > button,
    .stDownloadButton > button {{
        background: var(--mn-green);
        color: #061009;
        border: 1px solid var(--mn-green);
        border-radius: 9px;
        font-weight: 700;
        min-height: 42px;
        transition: all 0.2s ease;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        background: #00C968;
        color: #061009;
        border-color: #00C968;
        box-shadow: 0 0 18px rgba(0, 230, 118, 0.12);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        border-bottom: 1px solid var(--mn-border);
    }}

    .stTabs [data-baseweb="tab"] {{
        color: var(--mn-muted);
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
    }}

    .stTabs [aria-selected="true"] {{
        color: var(--mn-green) !important;
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: var(--mn-green);
    }}

    [data-testid="stDataFrame"] {{
        border: 1px solid var(--mn-border);
        border-radius: 10px;
        overflow: hidden;
    }}

    .stSelectbox label,
    .stMultiSelect label {{
        color: var(--mn-muted) !important;
        font-weight: 600;
    }}

    hr {{
        border-color: var(--mn-border);
        margin: 28px 0;
    }}

    .mn-footer {{
        border-top: 1px solid var(--mn-border);
        margin-top: 38px;
        padding: 20px 0 8px 0;
        color: var(--mn-muted);
        font-size: 12px;
        text-align: center;
    }}

    .mn-footer span {{
        color: var(--mn-green);
        font-weight: 700;
    }}

    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}

    @media (max-width: 640px) {{
        .mn-title {{
            letter-spacing: -1px;
        }}

        [data-testid="stMetric"] {{
            padding: 14px;
            min-height: 105px;
        }}

        [data-testid="stMetricValue"] {{
            font-size: 25px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# MARCA NA BARRA LATERAL
# =====================================================

with st.sidebar:
    st.markdown(
        """
        <div class="mn-brand">
            <div class="mn-logo">MN</div>
            <div>
                <div class="mn-brand-name">MN Scout</div>
                <div class="mn-brand-sub">ANALYTICS</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Painel de análise")
    st.caption("Explore os dados da partida.")

    st.divider()

    st.markdown("**FILTROS**")

    st.caption("Os filtros atualizam as estatísticas e os gráficos.")

    st.divider()

    st.markdown(
        """
        <div style="font-size:12px;color:#98A89D;line-height:1.8">
            <strong style="color:#00E676">MN LAB</strong><br>
            Tecnologia aplicada ao futebol.<br>
            Dados que ajudam a entender o jogo.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# CABECALHO
# =====================================================

st.markdown(
    """
    <div class="mn-eyebrow">FOOTBALL INTELLIGENCE / 01</div>
    <h1 class="mn-title">MN Scout <span>Analytics</span></h1>
    <p class="mn-description">
        Transforme eventos da partida em informações táticas.
        Explore finalizações, passes e desempenho individual.
    </p>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# CARREGAMENTO DOS DADOS
# =====================================================

if not ARQUIVO.exists():
    st.error(
        f"Arquivo de dados não encontrado: {ARQUIVO}. "
        "Execute primeiro: python baixar_dados.py"
    )
    st.stop()

try:
    eventos = load_events(ARQUIVO)
    df = events_to_dataframe(eventos)
except Exception as erro:
    st.error(f"Erro ao carregar os dados: {erro}")
    st.stop()

if df.empty:
    st.warning("Não existem eventos para analisar nesta partida.")
    st.stop()

equipes = sorted(df["team"].dropna().unique().tolist())

if not equipes:
    st.error("Nenhuma equipe foi encontrada nos dados.")
    st.stop()


# =====================================================
# FILTRO DE EQUIPE
# =====================================================

equipe_selecionada = st.sidebar.selectbox(
    "Equipe analisada",
    ["Todas as equipes"] + equipes,
)

equipe = (
    None
    if equipe_selecionada == "Todas as equipes"
    else equipe_selecionada
)

df_filtrado = (
    df.copy()
    if equipe is None
    else df[df["team"] == equipe].copy()
)


# =====================================================
# INDICADORES PRINCIPAIS
# =====================================================

st.markdown(
    '<div class="mn-section"><span>01</span> Visão geral</div>',
    unsafe_allow_html=True,
)

finalizacoes = df_filtrado[
    df_filtrado["event_type"] == "Shot"
]

gols = int(finalizacoes["is_goal"].fillna(False).sum())
total_finalizacoes = len(finalizacoes)
xg = float(finalizacoes["shot_xg"].sum())

passes = df_filtrado[
    df_filtrado["event_type"] == "Pass"
]

col1, col2, col3, col4 = st.columns(4)

col1.metric("GOLS", gols)
col2.metric("FINALIZAÇÕES", total_finalizacoes)
col3.metric("GOLS ESPERADOS (xG)", f"{xg:.2f}")
col4.metric("PASSES", len(passes))

st.caption(
    "Indicadores da equipe selecionada. "
    "xG corresponde à soma dos valores disponíveis no arquivo."
)

st.divider()


# =====================================================
# ESTATISTICAS DAS EQUIPES
# =====================================================

st.markdown(
    '<div class="mn-section"><span>02</span> Desempenho das equipes</div>',
    unsafe_allow_html=True,
)

resumo_equipes = get_team_summary(df)

if resumo_equipes.empty:
    st.info("Não há estatísticas de equipes disponíveis.")
else:
    st.dataframe(
        resumo_equipes,
        use_container_width=True,
        hide_index=True,
    )


# =====================================================
# JOGADORES
# =====================================================

st.markdown(
    '<div class="mn-section"><span>03</span> Análise de jogadores</div>',
    unsafe_allow_html=True,
)

resumo_jogadores = get_player_summary(df, team=equipe)

if resumo_jogadores.empty:
    st.info("Não há dados de jogadores disponíveis.")
else:
    st.dataframe(
        resumo_jogadores,
        use_container_width=True,
        hide_index=True,
    )


# =====================================================
# GRAFICOS TATICOS
# =====================================================

st.divider()

st.markdown(
    '<div class="mn-section"><span>04</span> Visualização tática</div>',
    unsafe_allow_html=True,
)

aba_finalizacoes, aba_passes = st.tabs(
    ["⚽ Mapa de finalizações", "➜ Mapa de passes"]
)

with aba_finalizacoes:
    fig = plot_shot_map(df, team=equipe)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with aba_passes:
    fig = plot_pass_map(df, team=equipe)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# =====================================================
# EXPORTACAO
# =====================================================

st.divider()

st.markdown(
    '<div class="mn-section"><span>05</span> Exportar análise</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style="color:#98A89D;font-size:14px">
        Exporte os eventos filtrados para continuar sua análise
        no Excel, Power BI ou Python.
    </p>
    """,
    unsafe_allow_html=True,
)

csv = df_filtrado.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="↓  Baixar dados em CSV",
    data=csv,
    file_name="mn_scout_analytics.csv",
    mime="text/csv",
)

# =====================================================
# RODAPE
# =====================================================

st.markdown(
    """
    <div class="mn-footer">
        <span>MN LAB</span> · MN Scout Analytics<br>
        Análise de dados aplicada ao futebol.
    </div>
    """,
    unsafe_allow_html=True,
)
