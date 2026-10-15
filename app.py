import pandas as pd
import streamlit as st

from src.load import get_engine

st.set_page_config(page_title="Dota 2 Pro Matches", layout="wide")
st.title("Dota 2 Pro Match Dashboard")


@st.cache_data
def query(sql):
    return pd.read_sql(sql, get_engine())


try:
    matches = query("SELECT * FROM pro_matches")
except Exception:
    st.error("Database not found. Run `python -m src.pipeline` first.")
    st.stop()

# Sidebar filter
only_known = st.sidebar.checkbox("Only matches with known teams", value=True)
if only_known:
    matches = matches[matches["teams_known"] == 1]

# Top numbers
col1, col2, col3 = st.columns(3)
col1.metric("Matches", len(matches))
col2.metric("Avg duration (min)", round(matches["duration_min"].mean(), 1))
col3.metric("Newest match (UTC)", str(matches["start_time"].max())[:16])

# Team wins
st.subheader("Teams with most wins")
wins = matches["winner"].value_counts().head(10)
st.bar_chart(wins)

# Hero stats
st.subheader("Most picked heroes")
min_picks = st.sidebar.slider("Minimum picks", 1, 20, 5)
heroes = query(
    """
    SELECT h.hero_name, COUNT(*) AS picks, ROUND(AVG(mp.won) * 100, 1) AS win_rate
    FROM match_players mp
    JOIN heroes h ON mp.hero_id = h.hero_id
    GROUP BY h.hero_name
    """
)
heroes = heroes[heroes["picks"] >= min_picks].sort_values("picks", ascending=False)
st.dataframe(heroes.head(15), use_container_width=True, hide_index=True)

# Recent matches
st.subheader("Recent matches")
st.dataframe(
    matches[["start_time", "league_name", "radiant_name", "dire_name", "winner"]].head(20),
    use_container_width=True,
    hide_index=True,
)