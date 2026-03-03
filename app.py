import streamlit as st
import pandas as pd

# ----------------------------------------------------
data = pd.read_csv("datasets/match_records.csv")
st.set_page_config(
    page_title='Analytics Dashboard'
)
st.title("ICC Men's T20 World Cup 2022 Matches | DashBoard")
st.divider()
# ----------------------------------------------------

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("WINNER", "ENGLAND", delta="+ SECOND TITLE")
with col2:
    st.metric("RUNNER UP", "PAKISTAN", delta="- LOOSE BY 5 WICKETS")
with col3:
    st.metric("PLAYER OF THE TOURNAMENT", "SAM CURRAN", delta="+ 13 WICKETS")
st.divider()

# ----------------------------------------------------

st.subheader("DataFrame Presentation")
st.dataframe(data)
st.divider()
# ----------------------------------------------------

st.subheader("Most Number Of Wins By A Team")
wins = {}
for team in data["winner"]:
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
for player in data["potm"]:
    potms[player] = potms.get(player, 0) + 1

potms = dict(sorted(potms.items(), key=lambda x:x[1], reverse=True)[:8])

potms_df = pd.DataFrame({'PLAYER': list(potms.keys()),
                         'NUMBER OF AWARDS': list(potms.values())})
potms_df = potms_df.dropna()

st.bar_chart(potms_df.set_index("PLAYER"))
st.divider()
# ----------------------------------------------------

st.caption("MADE BY TANISHK - A STUDENT AND A PROGRAMMER")