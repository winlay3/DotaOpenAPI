import json
import time
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://api.opendota.com/api"
RAW_DIR = Path("data/raw")
MATCHES_DIR = RAW_DIR / "matches"


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


def fetch_match_details(match_ids):
    """Download full details for each match, skipping ones we already have."""
    MATCHES_DIR.mkdir(parents=True, exist_ok=True)
    for match_id in match_ids:
        path = MATCHES_DIR / f"{match_id}.json"
        if path.exists():
            continue
        try:
            data = fetch(f"matches/{match_id}")
        except requests.RequestException as e:
            print(f"skipped match {match_id}: {e}")
            continue
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        time.sleep(1.1)  # stay under the API rate limit


def run(match_limit=50):
    datasets = {
        "heroes": "heroes",
        "pro_matches": "proMatches",
    }
    pro_matches = []
    for name, endpoint in datasets.items():
        data = fetch(endpoint)
        save_raw(data, f"{name}.json")
        if name == "pro_matches":
            pro_matches = data
        df = pd.DataFrame(data)
        print(f"{name}: {len(df)} rows, {len(df.columns)} columns")

    ids = [m["match_id"] for m in pro_matches[:match_limit]]
    fetch_match_details(ids)
    print(f"match details: {len(list(MATCHES_DIR.glob('*.json')))} files")


if __name__ == "__main__":
    run()