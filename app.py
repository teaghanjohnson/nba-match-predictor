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

# Load upcoming predictions
predictions = pd.read_csv('data/predictions.csv')
today = datetime.now().strftime("%Y-%m-%d")
games_today = (predictions['date'] == today).sum()
with model:
  st.write(f"MODEL ACCURACY 65.7% ")

with total:
  st.write(f"TOTAL PREDICTED {total_completed}")

with accuracy:
  st.write(f"LIVE ACCURACY {model_accuracy:.1f}% ")

with games:
  st.write(f"GAMES TODAY {games_today}")



team = st.selectbox("Select Team", list(TEAM_COLORS.keys()))


st.markdown(get_team_css(team), unsafe_allow_html=True)

st.markdown('<div class="team-header"><h2>Team Dashboard</h2></div>', unsafe_allow_html=True)

if team == 'NBA':
  st.write(predictions)
else:
  team_predictions = predictions[
    (predictions['home_abbrev'] == team) |
    (predictions['visitor_abbrev'] == team)
  ]
  st.write(team_predictions)

st.divider()
