import streamlit as st
import json
from os.path import join
import pandas as pd
from mplsoccer import Pitch, FontManager, add_image
from highlight_text import ax_text
from PIL import Image
from urllib.request import urlopen
from config import *

# a fontmanager object for using a google font
font_url = 'https://raw.githubusercontent.com/google/fonts/main/ofl/abel/Abel-Regular.ttf'
fm = FontManager(url=font_url)

SB_LOGO_URL = ('https://raw.githubusercontent.com/statsbomb/open-data/'
               'master/img/SB%20-%20Icon%20Lockup%20-%20Colour%20positive.png')
sb_logo = Image.open(urlopen(SB_LOGO_URL))

# Define the required parameters
required_params = ['competition_name', 'season_name', 'season_id', 'competition_id', 'match_id']

# Check if all required parameters exist in the session state
missing_params = [param for param in required_params if param not in st.session_state]

if missing_params:
    st.write(f"Missing parameters: {', '.join(missing_params)}")
    st.write(f"Please select the season, team and match before proceeding here.")
else:
    filename = join(STATSBOMB_DATA_DIR,"data","events",f"{st.session_state['match_id']}.json")
    with (open(filename) as f):
        data = json.load(f)
        events = pd.json_normalize(data)

        # Get all the fouls from the events dataframe
        foulss = events[events['type.name'] == 'Foul Committed']
        teams = foulss['team.name'].unique()

        # Create a copy of the original dataframe in order to avoid setting with copy warning
        fouls = foulss.copy()
        # Separate the location field to own columns
        fouls.loc[:,'location.x'] = fouls['location'].apply(lambda x: x[0])
        fouls.loc[:,'location.y'] = fouls['location'].apply(lambda x: x[1])
        

        # If you want to debug the fouls dataframe, you can print it out by uncommenting the line below
        # st.write(fouls)
        fouls_by_team = fouls.groupby('team.name')

        pitch = Pitch(pitch_type='statsbomb')
        fig, axs = pitch.grid(endnote_height=0.03, endnote_space=0,
                              title_height=0.10, title_space=0, ncols=2,
                              # Turn off the endnote/title axis. I usually do this after
                              # I am happy with the chart layout and text placement
                              axis=False,
                              grid_height=0.80)
        team_index = 0

        # Plot each team fouls into an own small pitch
        for name,fs in fouls_by_team:
            st.write(f"Fouls by {name}: {len(fs)}")
            scatter = pitch.scatter(fs['location.x'], fs['location.y'], ax=axs['pitch'][team_index], s=30, color='red', label='Foul')

            ax_text(60, -5, name, color='black', fontsize=20, ha='center', va='center', ax=axs['pitch'][team_index],fontproperties=fm.prop)
            team_index += 1

        # title text
        axs['title'].text(0.5, 0.65, f'{teams[0]} fouls vs {teams[1]}', fontsize=40,
                          fontproperties=fm.prop, va='center', ha='center')

        # endnote text
        axs['endnote'].text(0, 0.5, 'Team fouls - attacking direction is towards right',
                            fontsize=20, fontproperties=fm.prop, va='center', ha='left')

        # Add the statsbomb logo to the bottom right corner
        ax_sb_logo = add_image(sb_logo, fig, left=0.85,
                               # set the bottom and height to align with the endnote
                               bottom=axs['endnote'].get_position().y0,
                               height=axs['endnote'].get_position().height)

        st.pyplot(fig)





