
import pandas as pd


def get_team_summary(df):
    """Calcula estatísticas básicas por equipe."""
    if df.empty or "team" not in df.columns:
        return pd.DataFrame()

    resumo = []

    for equipe, dados in df.dropna(subset=["team"]).groupby("team"):
        finalizacoes = dados[dados["event_type"] == "Shot"]
        gols = int(finalizacoes["is_goal"].fillna(False).sum())

        passes = dados[dados["event_type"] == "Pass"]
        passes_completos = passes[
            passes["pass_outcome"].isna()
        ]

        xg = finalizacoes["shot_xg"].sum()

        resumo.append({
            "Equipe": equipe,
            "Gols": gols,
            "Finalizações": len(finalizacoes),
            "xG": round(float(xg), 2),
            "Passes": len(passes),
            "Passes completos": len(passes_completos),
        })

    return pd.DataFrame(resumo)


def get_player_summary(df, team=None):
    """Calcula estatísticas básicas por jogador."""
    if df.empty or "player" not in df.columns:
        return pd.DataFrame()

    dados = df.dropna(subset=["player"]).copy()

    if team:
        dados = dados[dados["team"] == team]

    resumo = []

    for jogador, eventos in dados.groupby("player"):
        finalizacoes = eventos[eventos["event_type"] == "Shot"]
        gols = int(finalizacoes["is_goal"].fillna(False).sum())

        passes = eventos[eventos["event_type"] == "Pass"]
        passes_completos = passes[passes["pass_outcome"].isna()]

        resumo.append({
            "Jogador": jogador,
            "Equipe": eventos["team"].dropna().iloc[0]
            if eventos["team"].notna().any() else "Não informada",
            "Gols": gols,
            "Finalizações": len(finalizacoes),
            "xG": round(float(finalizacoes["shot_xg"].sum()), 2),
            "Passes": len(passes),
            "Passes completos": len(passes_completos),
        })

    return (
        pd.DataFrame(resumo)
        .sort_values(
            ["Gols", "Finalizações"],
            ascending=False
        )
        .reset_index(drop=True)
    )
