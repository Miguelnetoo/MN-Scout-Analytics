
from pathlib import Path
import requests

BASE_URL = (
    "https://raw.githubusercontent.com/"
    "statsbomb/open-data/master/data"
)

PASTA = Path("data/matches")
PASTA.mkdir(parents=True, exist_ok=True)

sessao = requests.Session()
sessao.headers.update({
    "User-Agent": "MN-Scout-Analytics/1.0"
})


def buscar_json(url):
    resposta = sessao.get(url, timeout=30)
    resposta.raise_for_status()
    return resposta.json()


def main():
    print("Buscando competições disponíveis...")

    competicoes = buscar_json(
        f"{BASE_URL}/competitions.json"
    )

    if not competicoes:
        print("Nenhuma competição encontrada.")
        return

    print("\nCompetições disponíveis:")
    for i, comp in enumerate(competicoes[:10], start=1):
        print(
            f"{i}. {comp.get('competition_name')} "
            f"| Temporada: {comp.get('season_name')} "
            f"| IDs: {comp.get('competition_id')}/"
            f"{comp.get('season_id')}"
        )

    print("\nBuscando uma partida disponível...")

    # Procura partidas nas competições listadas.
    for comp in competicoes:
        comp_id = comp.get("competition_id")
        season_id = comp.get("season_id")

        url = (
            f"{BASE_URL}/matches/"
            f"{comp_id}/{season_id}.json"
        )

        try:
            partidas = buscar_json(url)
        except requests.RequestException:
            continue

        if not partidas:
            continue

        # Tenta primeiro a partida mais recente da lista.
        partidas = sorted(
            partidas,
            key=lambda p: p.get("match_date", ""),
            reverse=True
        )

        for partida in partidas:
            match_id = partida.get("match_id")

            if match_id is None:
                continue

            eventos_url = (
                f"{BASE_URL}/events/{match_id}.json"
            )

            try:
                resposta = sessao.get(
                    eventos_url,
                    timeout=45
                )

                if resposta.status_code == 404:
                    continue

                resposta.raise_for_status()
                eventos = resposta.json()

                if not isinstance(eventos, list) or not eventos:
                    continue

                arquivo = PASTA / "partida_01.json"
                arquivo.write_text(
                    resposta.text,
                    encoding="utf-8"
                )

                mandante = (
                    partida.get("home_team") or {}
                ).get("home_team_name", "Mandante")

                visitante = (
                    partida.get("away_team") or {}
                ).get("away_team_name", "Visitante")

                print("\nDownload concluído!")
                print(f"Partida: {mandante} x {visitante}")
                print(f"Data: {partida.get('match_date')}")
                print(f"ID numérico: {match_id}")
                print(f"Eventos: {len(eventos)}")
                print(f"Arquivo: {arquivo.resolve()}")
                return

            except (requests.RequestException, ValueError):
                continue

    print(
        "\nNão foi possível baixar uma partida. "
        "Verifique sua conexão e tente novamente."
    )


if __name__ == "__main__":
    main()
