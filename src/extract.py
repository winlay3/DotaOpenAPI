import json
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://api.opendota.com/api"
RAW_DIR = Path("data/raw")


def fetch(endpoint):
    """Fetch any OpenDota endpoint and return the parsed JSON."""
    response = requests.get(f"{BASE_URL}/{endpoint}", timeout=30)
    response.raise_for_status()
    return response.json()


def save_raw(data, filename):
    """Save the raw API response without changing it."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(RAW_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def run():
    datasets = {
        "heroes": "heroes",
        "pro_matches": "proMatches",
    }
    for name, endpoint in datasets.items():
        data = fetch(endpoint)
        save_raw(data, f"{name}.json")
        df = pd.DataFrame(data)
        print(f"{name}: {len(df)} rows, {len(df.columns)} columns")


if __name__ == "__main__":
    run()