
import matplotlib.pyplot as plt
from mplsoccer import Pitch


def plot_shot_map(df, team=None):
    """Desenha as finalizações no campo."""
    shots = df[df["event_type"] == "Shot"].copy()

    if team:
        shots = shots[shots["team"] == team]

    shots = shots.dropna(subset=["x", "y"])

    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="#101820",
        line_color="white",
        goal_type="box",
    )

    fig, ax = pitch.draw(figsize=(10, 7))
    fig.patch.set_facecolor("#101820")

    if not shots.empty:
        gols = shots["is_goal"].fillna(False).astype(bool)

        pitch.scatter(
            shots.loc[~gols, "x"],
            shots.loc[~gols, "y"],
            s=100,
            color="#00D084",
            edgecolors="white",
            linewidth=0.8,
            ax=ax,
            label="Finalização",
        )

        pitch.scatter(
            shots.loc[gols, "x"],
            shots.loc[gols, "y"],
            s=180,
            marker="*",
            color="#FFD166",
            edgecolors="white",
            linewidth=0.8,
            ax=ax,
            label="Gol",
        )

        ax.legend(
            loc="upper left",
            facecolor="#101820",
            labelcolor="white",
        )

    ax.set_title(
        "Mapa de finalizações",
        color="white",
        fontsize=16,
        pad=15,
    )

    fig.tight_layout()
    return fig


def plot_pass_map(df, team=None):
    """Desenha os passes e suas direções no campo."""
    passes = df[df["event_type"] == "Pass"].copy()

    if team:
        passes = passes[passes["team"] == team]

    passes = passes.dropna(
        subset=["x", "y", "end_x", "end_y"]
    )

    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="#101820",
        line_color="white",
        goal_type="box",
    )

    fig, ax = pitch.draw(figsize=(10, 7))
    fig.patch.set_facecolor("#101820")

    # Limita a quantidade de setas para manter o gráfico legível.
    if len(passes) > 250:
        passes = passes.sample(n=250, random_state=42)

    if not passes.empty:
        pitch.arrows(
            passes["x"],
            passes["y"],
            passes["end_x"],
            passes["end_y"],
            color="#00D084",
            alpha=0.65,
            width=1.5,
            headwidth=4,
            ax=ax,
        )

    ax.set_title(
        "Mapa de passes",
        color="white",
        fontsize=16,
        pad=15,
    )

    fig.tight_layout()
    return fig
