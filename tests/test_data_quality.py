import pandas as pd

PROCESSED = "data/processed"


def test_heroes_not_empty():
    heroes = pd.read_csv(f"{PROCESSED}/heroes.csv")
    assert len(heroes) > 100


def test_hero_ids_unique():
    heroes = pd.read_csv(f"{PROCESSED}/heroes.csv")
    assert heroes["hero_id"].is_unique


def test_match_ids_unique():
    matches = pd.read_csv(f"{PROCESSED}/pro_matches.csv")
    assert matches["match_id"].is_unique


def test_match_durations_positive():
    matches = pd.read_csv(f"{PROCESSED}/pro_matches.csv")
    assert (matches["duration_min"] > 0).all()


def test_winner_never_missing():
    matches = pd.read_csv(f"{PROCESSED}/pro_matches.csv")
    assert matches["winner"].notna().all()

def test_ten_players_per_match():
    players = pd.read_csv(f"{PROCESSED}/match_players.csv")
    assert (players.groupby("match_id").size() == 10).all()