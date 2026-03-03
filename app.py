import streamlit as st
import pandas as pd

# --------------------BASIC CONFIGURATION------------------------
match_records = pd.read_csv("dataset/match_records.csv")
batting_records = pd.read_csv("dataset/batting_records.csv")
bowling_records = pd.read_csv("dataset/bowling_records.csv")

st.set_page_config(
    page_title='Analytics Dashboard'
)
st.title("ICC Men's T20 World Cup 2022 Matches | DashBoard")
st.divider()
# -------------------------KPI METRICS ---------------------------

if "most_run_scorer" not in st.session_state:
    st.session_state.most_run_scorer = {}

if "most_wicket_taker" not in st.session_state:
    st.session_state.most_wicket_taker = {}

kpi = {"HOST": ["AUSTRALIA", "+ FIRST TIME"],
    "WINNER": ["ENGLAND", "+ SECOND TITLE"],
    "RUNNER UP": ["PAKISTAN", "- SECOND TIME"]}

pott = {"PLAYER": "SAM CURRAN",
        "CONTRIBUTION": "13 WICKETS"}

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("HOST", kpi["HOST"][0], delta=kpi["HOST"][1])
with col2:
    st.metric("WINNER", kpi["WINNER"][0], delta=kpi["WINNER"][1])
with col3:
    st.metric("RUNNER UP", kpi["RUNNER UP"][0], delta=kpi["RUNNER UP"][1])

with col1:
    if st.session_state.most_run_scorer:
        key1, val1 = list(st.session_state.most_run_scorer.items())[0]
        st.metric("MOST RUNS", key1, delta=f"+ {val1} RUNS")
with col2:
    if st.session_state.most_wicket_taker:
        key2, val2 = list(st.session_state.most_wicket_taker.items())[0]
        st.metric("MOST WICKETS", key2, delta=f"+ {val2} WICKETS")
with col3:
    key3, val3 = list(pott.items())[0]
    st.metric("PLAYER OF THE TOURNAMENT", key3, delta=f"+ {val3}")

st.divider()
# ---------------------DATAFRAME PRESENTATION------------------------

st.subheader("DataFrame Presentation")
with st.expander("VIEW MATCH RECORDS".title()):
    st.dataframe(match_records)
with st.expander("VIEW BATTING RECORDS".title()):
    st.dataframe(batting_records)
with st.expander("VIEW BOWLING RECORDS".title()):
    st.dataframe(bowling_records)

st.divider()
# ---------------------------MOST WINS-------------------------------

st.subheader("Most Number Of Wins By A Team")
wins = {}
for team in match_records["winner"]:
    wins[team] = wins.get(team, 0) + 1
del wins["abandoned"]
del wins["no result"]

wins = dict(sorted(wins.items(), key=lambda x:x[1], reverse=True)[: 10])

wins_df = pd.DataFrame({'TEAM': list(wins.keys()), 
                   'NUMBER OF WINS': list(wins.values())})

st.bar_chart(wins_df.set_index("TEAM"))
st.divider()
# ------------------------MOST POTM AWARDS----------------------------

st.subheader("Most Player Of The Match Awards")
potms = {}
for player in match_records["potm"]:
    potms[player] = potms.get(player, 0) + 1

potms = dict(sorted(potms.items(), key=lambda x:x[1], reverse=True)[:10])

potms_df = pd.DataFrame({'PLAYER': list(potms.keys()),
                         'NUMBER OF AWARDS': list(potms.values())})
potms_df = potms_df.dropna()

st.bar_chart(potms_df.set_index("PLAYER"))
st.divider()
# -------------------------HIGHEST RUN SCORER---------------------------

st.subheader("Highest Run Scorers")
highest_runs = {}

for player, run in zip(batting_records["batsmanName"], batting_records["runs"]):
    highest_runs[player.rstrip("(c)")] = highest_runs.get(player.rstrip("(c)"), 0) + run

highest_runs = dict(sorted(highest_runs.items(), key=lambda x:x[1], reverse=True)[:15])

runs_df = pd.DataFrame({"PLAYERS": list(highest_runs.keys()),
                    "RUNS": list(highest_runs.values())})

max_idx1 = runs_df["RUNS"].idxmax()
st.session_state.most_run_scorer = {runs_df.loc[max_idx1, "PLAYERS"]: runs_df.loc[max_idx1, "RUNS"]}

st.bar_chart(runs_df.set_index("PLAYERS"))
st.divider()
# ------------------------HIGHEST WICKET TAKER----------------------------

st.subheader("Highest Wicket Taker")
highest_wickets = {}

for player, wicket in zip(bowling_records["bowlerName"], bowling_records["wickets"]):
    highest_wickets[player.rstrip("(c)")] = highest_wickets.get(player.rstrip("(c)"), 0) + wicket

highest_wickets = dict(sorted(highest_wickets.items(), key=lambda x:x[1], reverse=True)[:15])

wickets_df = pd.DataFrame({"PLAYERS": list(highest_wickets.keys()),
                    "WICKETS": list(highest_wickets.values())})

max_idx2 = wickets_df["WICKETS"].idxmax()
st.session_state.most_wicket_taker = {wickets_df.loc[max_idx2, "PLAYERS"]: wickets_df.loc[max_idx2, "WICKETS"]}

st.bar_chart(wickets_df.set_index("PLAYERS"))
st.divider()
# ------------------------------------------------------------------------

st.caption("MADE BY TANISHK - A STUDENT AND A PROGRAMMER")
# ------------------------------------------------------------------------