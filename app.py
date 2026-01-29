from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from utils.constants.constants import TEAM_COLORS, get_team_css


col1, col2, col3 = st.columns([2, 5, 2])

with col1:
  team_image = st.empty()  # placeholder for team image

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

# get prediction history for specific team
correct = len(prediction_history[prediction_history['result'] == 'correct'])
incorrect = len(prediction_history[prediction_history['result'] == 'incorrect'])

# load upcoming predictions
predictions = pd.read_csv('data/predictions.csv')
today = datetime.now().strftime("%Y-%m-%d")
games_today = (predictions['date'] == today).sum()
with model:
  st.metric("MODEL ACCURACY", "66.02% ")

with total:
  st.metric("TOTAL PREDICTED", total_completed)

with accuracy:
  st.metric("LIVE ACCURACY" , f"{model_accuracy:.1f}% ")

with games:
  st.metric("GAMES TODAY", games_today)



team = st.selectbox("Select Team", list(TEAM_COLORS.keys()))
team_image.image(f"images/{team}.png", use_container_width=True)


st.markdown(get_team_css(team), unsafe_allow_html=True)

# columns to display (hide abbreviations for cleaner view)
display_cols = ['date', 'home', 'visitor', 'predicted_winner', 'confidence', 'result', 'actual_winner']

# filter predictions by team if not NBA
if team == 'NBA':
  filtered_predictions = predictions
else:
  filtered_predictions = predictions[
    (predictions['home_abbrev'] == team) |
    (predictions['visitor_abbrev'] == team)
  ]

# get this week's date range
from datetime import timedelta
today_date = datetime.now().date()
week_end = today_date + timedelta(days=7)

# filter for today and this week
predictions['date_parsed'] = pd.to_datetime(predictions['date']).dt.date
today_games = filtered_predictions[pd.to_datetime(filtered_predictions['date']).dt.date == today_date]
week_games = filtered_predictions[
  (pd.to_datetime(filtered_predictions['date']).dt.date >= today_date) &
  (pd.to_datetime(filtered_predictions['date']).dt.date <= week_end)
]

st.divider()

# initialize session state for active tab
if 'active_tab' not in st.session_state:
  st.session_state.active_tab = 'today'

# button row
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

with btn_col1:
  if st.button("Today", use_container_width=True):
    st.session_state.active_tab = 'today'

with btn_col2:
  if st.button("This Week", use_container_width=True):
    st.session_state.active_tab = 'week'

with btn_col3:
  if st.button("Model Performance", use_container_width=True):
    st.session_state.active_tab = 'performance'

with btn_col4:
  if st.button("All Predictions", use_container_width=True):
    st.session_state.active_tab = 'all'

st.divider()

# content based on active tab
if st.session_state.active_tab == 'today':
  st.markdown('<div class="team-header"><h2>Today\'s Games</h2></div>', unsafe_allow_html=True)
  if len(today_games) > 0:
    st.dataframe(today_games[display_cols], use_container_width=True, hide_index=True)
  else:
    st.info("No games scheduled for today")

elif st.session_state.active_tab == 'week':
  st.markdown('<div class="team-header"><h2>This Week\'s Games</h2></div>', unsafe_allow_html=True)
  if len(week_games) > 0:
    st.dataframe(week_games[display_cols], use_container_width=True, hide_index=True)
  else:
    st.info("No games scheduled this week")

elif st.session_state.active_tab == 'performance':
  st.markdown('<div class="team-header"><h2>Model Performance</h2></div>', unsafe_allow_html=True)

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

elif st.session_state.active_tab == 'all':
  st.markdown('<div class="team-header"><h2>All Predictions</h2></div>', unsafe_allow_html=True)
  st.dataframe(filtered_predictions[display_cols], use_container_width=True, hide_index=True)

