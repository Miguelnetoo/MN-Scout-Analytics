
from src.data_loader import load_events, events_to_dataframe

# Caminho do arquivo baixado pelo script baixar_dados.py
arquivo = "data/matches/partida_01.json"

try:
    # Carrega os eventos da partida
    eventos = load_events(arquivo)

    # Converte os eventos em um DataFrame
    df = events_to_dataframe(eventos)

    print("=" * 50)
    print("TESTE DOS DADOS - MN SCOUT ANALYTICS")
    print("=" * 50)

    print(f"\nTotal de eventos: {len(df)}")

    print("\n--- Tipos de eventos mais frequentes ---")
    print(df["event_type"].value_counts().head(10))

    print("\n--- Primeiros 5 registros ---")
    print(df.head().to_string(index=False))

    print("\n--- Equipes encontradas ---")
    print(df["team"].dropna().unique())

    print("\n--- Jogadores encontrados ---")
    print("Total de jogadores:", df["player"].nunique())

    print("\n--- Finalizações ---")
    finalizacoes = df[df["event_type"] == "Shot"]
    print("Total de finalizações:", len(finalizacoes))

    print("\n--- Gols ---")
    print("Total de gols:", int(df["is_goal"].sum()))

    print("\n--- Resultado do teste ---")
    print("SUCESSO! Os dados foram carregados corretamente.")

except FileNotFoundError:
    print(f"ERRO: Arquivo não encontrado: {arquivo}")
    print("Execute primeiro: python baixar_dados.py")

except Exception as erro:
    print("ERRO ao testar os dados:")
    print(f"{type(erro).__name__}: {erro}")
