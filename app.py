from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from utils.constants.constants import TEAM_COLORS, get_team_css

st.title("NBA MATCH PREDICTOR")
st.subheader("ML-Powered Game Predictions")
st.divider()

team = st.selectbox("Select Team", list(TEAM_COLORS.keys()))

st.markdown(get_team_css(team), unsafe_allow_html=True)

st.markdown('<div class="team-header"><h2>Team Dashboard</h2></div>', unsafe_allow_html=True)
