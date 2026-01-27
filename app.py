from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from utils.constants.constants import TEAM_COLORS, get_team_css

col1, col2, col3 = st.columns([2, 5, 2])

with col1:
  st.image("images/nba-logo.png", use_container_width=True)

with col2:
  st.title("NBA MATCH PREDICTOR")
  st.caption("ML-Powered Game Predictions")

with col3:
  st.markdown(f"**Updated:** {datetime.now().strftime('%b %d')}")

st.divider()

model, total, accuracy, games =  st.columns([3,3,3,3])

# Load prediction history for accuracy stats
prediction_history = pd.read_csv('data/prediction_history.csv')
correct = len(prediction_history[prediction_history['result'] == 'correct'])
incorrect = len(prediction_history[prediction_history['result'] == 'incorrect'])
total_completed = correct + incorrect
model_accuracy = correct / total_completed * 100 if total_completed > 0 else 0

# load upcoming predictions
predictions = pd.read_csv('data/predictions.csv')
today = datetime.now().strftime("%Y-%m-%d")
games_today = (predictions['date'] == today).sum()
with model:
  st.metric("MODEL ACCURACY", "65.7% ")

with total:
  st.metric("TOTAL PREDICTED", total_completed)

with accuracy:
  st.metric("LIVE ACCURACY" , f"{model_accuracy:.1f}% ")

with games:
  st.metric("GAMES TODAY", games_today)



team = st.selectbox("Select Team", list(TEAM_COLORS.keys()))


st.markdown(get_team_css(team), unsafe_allow_html=True)

st.markdown('<div class="team-header"><h2>Upcoming Game Predictions</h2></div>', unsafe_allow_html=True)

if team == 'NBA':
  st.write(predictions)
else:
  team_predictions = predictions[
    (predictions['home_abbrev'] == team) |
    (predictions['visitor_abbrev'] == team)
  ]
  st.write(team_predictions)

st.divider()

# MODEL PERFORMANCE CHARTS

# load and prepare history data for charts
history_df = pd.read_csv('data/prediction_history.csv')
history_df['date'] = pd.to_datetime(history_df['date'])
history_df = history_df.sort_values('date')

# create win column (1 for correct, 0 for incorrect)
history_df['win'] = (history_df['result'] == 'correct').astype(int)

# cumulative stats
history_df['cumulative_wins'] = history_df['win'].cumsum()
history_df['cumulative_losses'] = (~history_df['win'].astype(bool)).cumsum()
history_df['cumulative_total'] = range(1, len(history_df) + 1)
history_df['cumulative_pct'] = history_df['cumulative_wins'] / history_df['cumulative_total'] * 100

# rolling accuracy for different windows
for w in [10, 25, 50]:
    history_df[f'rolling_accuracy_{w}'] = history_df['win'].rolling(window=w, min_periods=1).mean() * 100

# rolling accuracy chart
st.subheader("Model Performance")
window = st.select_slider("Rolling Window", options=[10, 25, 50], value=25)

rolling_chart = alt.Chart(history_df).mark_line(color='#1f77b4').encode(
    x=alt.X('date:T', title='Date'),
    y=alt.Y(f'rolling_accuracy_{window}:Q', title=f'Accuracy %', scale=alt.Scale(domain=[0, 100])),
    tooltip=[
        alt.Tooltip('date:T', title='Date'),
        alt.Tooltip(f'rolling_accuracy_{window}:Q', title='Accuracy %', format='.1f')
    ]
).properties(title=f'Rolling Accuracy (Last {window} Games)')

st.altair_chart(rolling_chart, use_container_width=True)

# cumulative chart
metric = st.radio("Show", ["Cumulative Win %", "Cumulative Correct Picks"], horizontal=True)

if metric == "Cumulative Win %":
    cumulative_chart = alt.Chart(history_df).mark_line(color='#2ca02c').encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('cumulative_pct:Q', title='Win %', scale=alt.Scale(domain=[0, 100])),
        tooltip=[
            alt.Tooltip('date:T', title='Date'),
            alt.Tooltip('cumulative_pct:Q', title='Win %', format='.1f'),
            alt.Tooltip('cumulative_wins:Q', title='Correct'),
            alt.Tooltip('cumulative_losses:Q', title='Incorrect')
        ]
    ).properties(title='Cumulative Win Percentage')
else:
    cumulative_chart = alt.Chart(history_df).mark_line(color='#2ca02c').encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('cumulative_wins:Q', title='Correct Picks'),
        tooltip=[
            alt.Tooltip('date:T', title='Date'),
            alt.Tooltip('cumulative_wins:Q', title='Correct'),
            alt.Tooltip('cumulative_losses:Q', title='Incorrect')
        ]
    ).properties(title='Cumulative Correct Picks')

st.altair_chart(cumulative_chart, use_container_width=True)

