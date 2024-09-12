import streamlit as st
import json
from streamlit_extras.switch_page_button import switch_page
from os.path import join
from config import *


# Define the required parameters
required_params = ['competition_name', 'season_name', 'season_id', 'competition_id']

# Check if all required parameters exist in the session state
missing_params = [param for param in required_params if param not in st.session_state]

if missing_params:
    st.write(f"Missing parameters: {', '.join(missing_params)}")
else:
    filename = join(STATSBOMB_DATA_DIR,"data","matches", f"{st.session_state['competition_id']}", f"{st.session_state['season_id']}.json")
    with open(filename) as f:
        data = json.load(f)

    # Find all the distinct teams from home and away teams by adding them into a set
    teams = set()
    for match in data:
        teams.add(match['home_team']['home_team_name'])
        teams.add(match['away_team']['away_team_name'])

    # Ask for the user to select one
    selected_team = st.selectbox("Please select a team", list(teams))

    # Filter matches where the selected team has played
    f_m = [match for match in data if match['home_team']['home_team_name'] == selected_team or match['away_team']['away_team_name'] == selected_team]

    # Create a dictionary of matches with the match date and the match id
    matches = {(f"{item['match_date']}: {item['home_team']['home_team_name']} vs {item['away_team']['away_team_name']}"):item['match_id'] for item in f_m}

    # Ask for the user to select one
    selected_match = st.selectbox("Please select a match", list(matches))

    # Open the match visualization page with a button press
    open_match = st.button("Investigate the selected match")
    if open_match:
        #switch_page("Matches_for_competition")
        st.write(matches[selected_match])
        st.session_state['match_id'] = matches[selected_match]
        st.write("Investigating the selected match...")
        switch_page("Visualize match stats")

    