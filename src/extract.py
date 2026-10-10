import json
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://api.opendota.com/api"
RAW_DIR = Path("data/raw")


def fetch_heroes():
    """Fetch the list of all heroes from the OpenDota API."""
    response = requests.get(f"{BASE_URL}/heroes", timeout=30)
    response.raise_for_status()  # stops with an error if the request failed
    return response.json()


def save_raw(data, filename):
    """Save the raw API response without changing it."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(RAW_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    heroes = fetch_heroes()
    save_raw(heroes, "heroes.json")
    df = pd.DataFrame(heroes)
    print(df.head())
    print(f"Total heroes: {len(df)}")