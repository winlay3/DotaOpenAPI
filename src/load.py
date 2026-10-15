from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

PROCESSED_DIR = Path("data/processed")
DB_PATH = Path("data/warehouse.db")


def get_engine():
    return create_engine(f"sqlite:///{DB_PATH}")


def run():
    engine = get_engine()

    heroes = pd.read_csv(PROCESSED_DIR / "heroes.csv")
    matches = pd.read_csv(PROCESSED_DIR / "pro_matches.csv", parse_dates=["start_time"])

    # if_exists="replace" rebuilds the table each run, so reruns are safe
    heroes.to_sql("heroes", engine, if_exists="replace", index=False)
    matches.to_sql("pro_matches", engine, if_exists="replace", index=False)

    players = pd.read_csv(PROCESSED_DIR / "match_players.csv")
    players.to_sql("match_players", engine, if_exists="replace", index=False)
    print(f"match_players: {len(players)} rows loaded")

    print(f"heroes: {len(heroes)} rows loaded")
    print(f"pro_matches: {len(matches)} rows loaded")


if __name__ == "__main__":
    run()