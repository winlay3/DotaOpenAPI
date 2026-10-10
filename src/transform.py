from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def transform_heroes():
    df = pd.read_json(RAW_DIR / "heroes.json")
    df["name"] = df["name"].str.replace("npc_dota_hero_", "", regex=False)
    df["role_count"] = df["roles"].apply(len)
    df["roles"] = df["roles"].apply(lambda r: ", ".join(r))
    return df.rename(
        columns={"id": "hero_id", "name": "hero_key", "localized_name": "hero_name"}
    )


def transform_pro_matches():
    # convert_dates=False so pandas doesn't guess the time format for us
    df = pd.read_json(RAW_DIR / "pro_matches.json", convert_dates=False)
    df = df.drop_duplicates(subset="match_id")
    df["start_time"] = pd.to_datetime(df["start_time"], unit="s")
    df["duration_min"] = (df["duration"] / 60).round(1)
    df["radiant_name"] = df["radiant_name"].fillna("Unknown")
    df["dire_name"] = df["dire_name"].fillna("Unknown")
    df["winner"] = df["radiant_name"].where(df["radiant_win"], df["dire_name"])
    return df[
        [
            "match_id", "start_time", "duration_min", "league_name",
            "radiant_name", "dire_name", "radiant_score", "dire_score",
            "radiant_win", "winner",
        ]
    ]


def run():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    tables = {
        "heroes": transform_heroes(),
        "pro_matches": transform_pro_matches(),
    }
    for name, df in tables.items():
        df.to_csv(PROCESSED_DIR / f"{name}.csv", index=False)
        print(f"{name}: {len(df)} rows saved")


if __name__ == "__main__":
    run()