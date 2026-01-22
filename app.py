from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
st.title("Enjoy Basketball")
st.subheader("This is my nba-match predictor predicting " \
"all the 2025-2026 NBA games")


chart_data = pd.read_csv("data/predictions.csv"
  
  )

st.write(chart_data.head(3))


selected_teams = st.multiselect(
  "what are your favourite teams",
  ["Raptors", "Knicks", "Lakers", "Celtics"]
)

st.write(selected_teams)
