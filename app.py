import streamlit as st
import pandas as pd

# --------------------------FUNCTIONAL PROGRAMMING--------------------------
def load_data(edition_year: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    match_records = pd.read_csv(f"dataset/{edition_year}/match_records.csv")
    batting_records = pd.read_csv(f"dataset/{edition_year}/batting_records.csv")
    bowling_records = pd.read_csv(f"dataset/{edition_year}/bowling_records.csv")
    kpi_data = pd.read_json(f"dataset/{edition_year}/kpi_data.json")

    return match_records, batting_records, bowling_records, kpi_data

def most_wins(match_records : pd.DataFrame) -> pd.DataFrame:
    wins = {}
    for team in match_records["winner"]:
        wins[team] = wins.get(team, 0) + 1
    if "abandoned" in wins: del wins["abandoned"]
    if "no result" in wins: del wins["no result"]

    wins = dict(sorted(wins.items(), key=lambda x:x[1], reverse=True)[: 10])

    df = pd.DataFrame({'TEAM': list(wins.keys()), 
                    'NUMBER OF WINS': list(wins.values())})
    return df

def most_potm(match_records : pd.DataFrame) -> pd.DataFrame:
    potms = {}
    for player in match_records["potm"]:
        potms[player] = potms.get(player, 0) + 1

    potms = dict(sorted(potms.items(), key=lambda x:x[1], reverse=True)[:10])

    df = pd.DataFrame({'PLAYER': list(potms.keys()),
                            'NUMBER OF AWARDS': list(potms.values())})
    df = df.dropna()
    return df

def most_runs(batting_records: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    highest_runs = {}

    for player, run in zip(batting_records["batsmanName"], batting_records["runs"]):
        highest_runs[player.rstrip("(c)")] = highest_runs.get(player.rstrip("(c)"), 0) + run

    highest_runs = dict(sorted(highest_runs.items(), key=lambda x:x[1], reverse=True)[:15])

    df = pd.DataFrame({"PLAYERS": list(highest_runs.keys()),
                        "RUNS": list(highest_runs.values())})

    max_idx = df["RUNS"].idxmax()
    kpi = {df.loc[max_idx, "PLAYERS"]: df.loc[max_idx, "RUNS"]}
    return (df, kpi)

def most_wickets(bowling_records: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    highest_wickets = {}
    for player, wicket in zip(bowling_records["bowlerName"], bowling_records["wickets"]):
        highest_wickets[player.rstrip("(c)")] = highest_wickets.get(player.rstrip("(c)"), 0) + wicket

    highest_wickets = dict(sorted(highest_wickets.items(), key=lambda x:x[1], reverse=True)[:15])

    df = pd.DataFrame({"PLAYERS": list(highest_wickets.keys()),
                        "WICKETS": list(highest_wickets.values())})

    max_idx = df["WICKETS"].idxmax()
    kpi = {df.loc[max_idx, "PLAYERS"]: df.loc[max_idx, "WICKETS"]}
    return (df, kpi)

# ---------------------------STREAMLIT RENDERING-----------------------------

st.set_page_config(page_title='Analytics Dashboard')

with st.sidebar:
    edition_year = st.selectbox("SELECT THE EDITION TO ANALYZE",["2022", "2024"])

st.title(f"ICC Men's T20 World Cup {edition_year} DashBoard")
st.divider()

match_records, batting_records, bowling_records, kpi_data = load_data(edition_year)
high_run_scorer = list(most_runs(batting_records)[1].items())
high_wicket_taker = list(most_wickets(bowling_records)[1].items())

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("HOST", kpi_data["HOST"][0], delta=kpi_data["HOST"][1])
with col2:
    st.metric("WINNER", kpi_data["WINNER"][0], delta=kpi_data["WINNER"][1])
with col3:
    st.metric("RUNNER UP", kpi_data["RUNNER UP"][0], delta=kpi_data["RUNNER UP"][1])

with col1:
    st.metric("MOST RUNS", high_run_scorer[0][0], delta=f"+ {high_run_scorer[0][1]} RUNS")
with col2:
    st.metric("MOST WICKETS", high_wicket_taker[0][0], delta=f"+ {high_wicket_taker[0][1]} WICKETS")
with col3:
    st.metric("PLAYER OF THE TOURNAMENT", kpi_data["POTT"][0], delta=kpi_data["POTT"][1])

st.divider()

st.subheader("DataFrame Presentation")
with st.expander("View Match Records"):
    st.dataframe(match_records)
with st.expander("View Batting Records"):
    st.dataframe(batting_records)
with st.expander("View Bowling Records"):
    st.dataframe(bowling_records)
    
st.divider()

st.subheader("Most Number Of Wins By A Team")
most_wins_df = most_wins(match_records)
st.bar_chart(most_wins_df.set_index("TEAM"))
st.divider()

st.subheader("Most Player Of The Match Awards")
most_potm_df = most_potm(match_records)
st.bar_chart(most_potm_df.set_index("PLAYER"))
st.divider()

st.subheader("Highest Run Scorers")
most_runs_df = most_runs(batting_records)[0]
st.bar_chart(most_runs_df.set_index("PLAYERS"))
st.divider()

st.subheader("Highest Wicket Taker")
most_wickets_df = most_wickets(bowling_records)[0]
st.bar_chart(most_wickets_df.set_index("PLAYERS"))
st.divider()

st.caption("MADE BY TANISHK - A STUDENT AND A PROGRAMMER")
# ---------------------------------------------------------------------------