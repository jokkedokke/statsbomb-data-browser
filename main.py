import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import json
from os.path import join
from config import *

st.title('Hello World')

# We use a path joining library in order to avoid operating system specific
# file path issues between Windows and MacOS
filename = join(STATSBOMB_DATA_DIR,"data","competitions.json")
with open(filename) as f:
    data = json.load(f)

options = {item['competition_name']: item['competition_id'] for item in data}
selected_competition = st.selectbox('Select a competition', options)
selected_id = options[selected_competition]

# Get all the seasons for the selected competition id from the original data json
seasons = {item['season_name']: item['season_id'] for item in data if item['competition_id'] == selected_id}

selected_season = st.selectbox('Select a competition season', seasons)
s_id = seasons[selected_season]

# Store the selected competition and season info into the session state,
# Which can be shared with the other pages inside the streamlit application
st.session_state['competition_name'] = selected_competition
st.session_state['season_name'] = selected_season
st.session_state['season_id'] = s_id
st.session_state['competition_id'] = selected_id

open_season = st.button("Browse matches in the selected season")
if open_season:
    switch_page("Matches_for_competition")