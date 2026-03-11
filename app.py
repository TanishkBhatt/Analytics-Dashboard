import streamlit as st
import pandas as pd

# --------------------------FUNCTIONAL PROGRAMMING--------------------------
def load_tournament_data(edition_year: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    match_records = pd.read_csv(f"dataset/{edition_year}/match_records.csv")
    kpi_data = pd.read_json(f"dataset/{edition_year}/kpi_data.json")
    return match_records, kpi_data

def load_performance_data():
    pass

def most_wins_data(match_records : pd.DataFrame) -> pd.DataFrame:
    wins = {}
    for team in match_records["winner"]:
        wins[team] = wins.get(team, 0) + 1
    if "abandoned" in wins: del wins["abandoned"]
    if "no result" in wins: del wins["no result"]

    wins = dict(sorted(wins.items(), key=lambda x:x[1], reverse=True)[: 10])
    df = pd.DataFrame({'TEAM': list(wins.keys()), 
                    'NUMBER OF WINS': list(wins.values())})
    return df

def most_potm_data(match_records : pd.DataFrame) -> pd.DataFrame:
    potms = {}
    for player in match_records["potm"]:
        potms[player] = potms.get(player, 0) + 1

    potms = dict(sorted(potms.items(), key=lambda x:x[1], reverse=True)[:10])
    df = pd.DataFrame({'PLAYER': list(potms.keys()),
                            'NUMBER OF AWARDS': list(potms.values())})
    return df.dropna()

# ---------------------------STREAMLIT RENDERING-----------------------------

st.set_page_config(page_title='Analytics Dashboard')
with st.sidebar:
    edition_year = st.selectbox("SELECT THE EDITION TO ANALYZE",["2022", "2024", "2026"])

st.title(f"ICC Men's T20 World Cup {edition_year} DashBoard")
st.divider()

match_records, kpi_data = load_tournament_data(edition_year)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("HOST", kpi_data["HOST"][0], delta=kpi_data["HOST"][1])
    st.metric("MOST RUNS", kpi_data["MOST RUNS"][0], delta=kpi_data["MOST RUNS"][1])
with col2:
    st.metric("WINNER", kpi_data["WINNER"][0], delta=kpi_data["WINNER"][1])
    st.metric("MOST WICKETS", kpi_data["MOST WICKETS"][0], delta=kpi_data["MOST WICKETS"][1])
with col3:
    st.metric("RUNNER UP", kpi_data["RUNNER UP"][0], delta=kpi_data["RUNNER UP"][1])
    st.metric("PLAYER OF THE TOURNAMENT", kpi_data["POTT"][0], delta=kpi_data["POTT"][1])

st.divider()

st.subheader("DataFrame Presentation")
with st.expander("View Match Records"):
    st.dataframe(match_records)
st.divider()

st.subheader("Most Number Of Wins By A Team")
most_wins = most_wins_data(match_records)
with st.expander("View DataFrame"):
    st.dataframe(most_wins)
st.write("")
st.bar_chart(most_wins.set_index("TEAM"))
st.divider()

st.subheader("Most Player Of The Match Awards")
most_potm = most_potm_data(match_records)
with st.expander("View DataFrame"):
    st.dataframe(most_potm)
st.write("")
st.bar_chart(most_potm.set_index("PLAYER"))
st.divider()

st.caption("MADE BY TANISHK - A STUDENT AND A PROGRAMMER")
# ---------------------------------------------------------------------------