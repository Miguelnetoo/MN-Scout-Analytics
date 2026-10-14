
import json
from pathlib import Path

import pandas as pd


def load_events(file_path):
    """Carrega os eventos de uma partida do arquivo JSON."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo da partida não encontrado: {path}"
        )

    with path.open("r", encoding="utf-8") as arquivo:
        events = json.load(arquivo)

    if not isinstance(events, list):
        raise ValueError(
            "O arquivo JSON não contém uma lista de eventos válida."
        )

    return events


def extract_location(value):
    """Extrai as coordenadas x e y de uma localização."""
    if isinstance(value, dict):
        value = value.get("location")

    if isinstance(value, list) and len(value) >= 2:
        try:
            if value[0] is not None and value[1] is not None:
                return float(value[0]), float(value[1])
        except (TypeError, ValueError):
            pass

    return None, None


def events_to_dataframe(events):
    """Converte os eventos do StatsBomb em um DataFrame."""
    rows = []

    for event in events:
        event_type = event.get("type") or {}
        team = event.get("team") or {}
        player = event.get("player") or {}
        pass_data = event.get("pass") or {}
        shot_data = event.get("shot") or {}

        x, y = extract_location(event.get("location"))
        end_x, end_y = extract_location(
            pass_data.get("end_location")
        )

        outcome = (
            pass_data.get("outcome")
            or shot_data.get("outcome")
            or {}
        )

        shot_xg = shot_data.get("statsbomb_xg")
        if shot_xg is None:
            shot_xg = shot_data.get("xg")

        rows.append({
            "event_id": event.get("id"),
            "period": event.get("period"),
            "minute": event.get("minute"),
            "second": event.get("second"),
            "team": team.get("name"),
            "player": player.get("name"),
            "event_type": event_type.get("name"),
            "possession": event.get("possession"),
            "play_pattern": (
                event.get("play_pattern") or {}
            ).get("name"),
            "x": x,
            "y": y,
            "end_x": end_x,
            "end_y": end_y,
            "pass_outcome": outcome.get("name"),
            "shot_xg": shot_xg,
            "is_goal": (
                event_type.get("name") == "Shot"
                and shot_data.get("outcome", {}).get("name")
                == "Goal"
            ),
        })

    df = pd.DataFrame(rows)

    if not df.empty:
        df["minute"] = pd.to_numeric(
            df["minute"], errors="coerce"
        )
        df["shot_xg"] = pd.to_numeric(
            df["shot_xg"], errors="coerce"
        )

    return df
