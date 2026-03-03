import streamlit as st
import pandas as pd

# ----------------------------------------------------
match_records = pd.read_csv("dataset/match_records.csv")
batting_records = pd.read_csv("dataset/batting_records.csv")
bowling_records = pd.read_csv("dataset/bowling_records.csv")

st.set_page_config(
    page_title='Analytics Dashboard'
)
st.title("ICC Men's T20 World Cup 2022 Matches | DashBoard")
st.divider()
# ----------------------------------------------------

if "most_run_scorer" and "most_wicket_taker" not in st.session_state:
    st.session_state.most_run_scorer = None
    st.session_state.most_wicket_taker = None

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("HOST", "AUSTRALIA", delta="+ FIRST TIME")
with col2:
    st.metric("WINNER", "ENGLAND", delta="+ SECOND TITLE")
with col3:
    st.metric("RUNNER UP", "PAKISTAN", delta="- SECOND TIME")
with col1:
    st.metric("MOST RUNS", most_run_scorer, delta="+ RUNS")
with col2:
    st.metric("MOST WICKETS", most_wicket_taker, delta="+ WICKETS")
with col3:
    st.metric("PLAYER OF THE TOURNAMENT", "SAM CURRAN", delta="+ 13 WICKETS")
st.divider()

# ----------------------------------------------------

st.subheader("DataFrame Presentation")
with st.expander("VIEW MATCH RECORDS".title()):
    st.dataframe(match_records)
with st.expander("VIEW BATTING RECORDS".title()):
    st.dataframe(batting_records)
with st.expander("VIEW BOWLING RECORDS".title()):
    st.dataframe(bowling_records)
st.divider()
# ----------------------------------------------------

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
# ----------------------------------------------------

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
# ----------------------------------------------------

st.subheader("Highest Run Scorers")
highest_runs = {}

for player, run in zip(batting_records["batsmanName"], batting_records["runs"]):
    highest_runs[player.rstrip("(c)")] = highest_runs.get(player.rstrip("(c)"), 0) + run

highest_runs = dict(sorted(highest_runs.items(), key=lambda x:x[1], reverse=True)[:15])

runs_df = pd.DataFrame({"PLAYERS": list(highest_runs.keys()),
                    "RUNS": list(highest_runs.values())})

st.session_state.most_run_scorer = runs_df.loc[runs_df["RUNS"].idxmax(), "PLAYERS"]
st.rerun()

st.bar_chart(runs_df.set_index("PLAYERS"))
st.divider()
# ----------------------------------------------------

st.subheader("Highest Wicket Taker")
highest_wickets = {}

for player, wicket in zip(bowling_records["bowlerName"], bowling_records["wickets"]):
    highest_wickets[player.rstrip("(c)")] = highest_wickets.get(player.rstrip("(c)"), 0) + wicket

highest_wickets = dict(sorted(highest_wickets.items(), key=lambda x:x[1], reverse=True)[:15])

wickets_df = pd.DataFrame({"PLAYERS": list(highest_wickets.keys()),
                    "WICKETS": list(highest_wickets.values())})

st.session_state.most_wicket_taker = wickets_df.loc[wickets_df["WICKETS"].idxmax(), "PLAYERS"]
st.rerun()

st.bar_chart(wickets_df.set_index("PLAYERS"))
st.divider()
# -----------------------------------------------------

st.caption("MADE BY TANISHK - A STUDENT AND A PROGRAMMER")
# -----------------------------------------------------