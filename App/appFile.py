import pandas as pd
import numpy as np
import streamlit as st
from app_functions import plot_scatter
from pathlib import Path
import ast
st.set_page_config(layout='wide')



DATA_PATH = Path("data/merged_season_data.csv")
MODEL_PATH = Path("data/model_performance_summary.csv")

@st.cache_data(ttl=30)  # re-read at most every 30s; adjust as needed
def load_csv(path: Path, sep=","):
    return pd.read_csv(path, sep=sep)

# Initialize keys once (don’t clobber user/session edits on every rerun)
st.session_state.setdefault('data', pd.DataFrame())
st.session_state.setdefault('model', pd.DataFrame())

# Load (cached) data
st.session_state['data'] = load_csv(DATA_PATH)
st.session_state['model'] = load_csv(MODEL_PATH)

## App title
st.title("KAA GENT - TRANSFER VALUE ANALYSIS APP")
# Optional: manual refresh button to force a cache clear + rerun
if st.button("Refresh data"):
    st.cache_data.clear()
    st.rerun()

## select position
selected_position = st.selectbox("Select position to analyze", st.session_state['model']['position'].unique().tolist())

## select season
selected_season = st.selectbox("Select season to analyze: ", st.session_state['data']['season_name'].unique().tolist())

## filter model information based on selected position
model_filtered = st.session_state['model'][st.session_state['model']['position'] == selected_position]
nsamples = model_filtered['samples'].values[0]
r2 = model_filtered['R²'].values[0]
model_features = ast.literal_eval(model_filtered['top_features_clean'].values[0])
data_filtered = st.session_state['data'][(st.session_state['data']['primary_position_group'] == selected_position) &
                                         (st.session_state['data']['season_name'] == selected_season)]
data_filtered.columns = [
    x.replace("player_season_", "").replace("_90", "").replace("_"," ").title()
    if "player_season" in x else x for x in data_filtered.columns
]

data_filtered.columns = [x.replace("Improvement","(I)")
                         if "Improve" in x else x for x in data_filtered.columns]
data_vars = [x for x in data_filtered.columns if '_' not in x]

tab1, tab2 = st.tabs(['Exploration', 'Model Based Analysis'])
with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        x_axis = st.selectbox("Select X-axis metric", data_vars, key='x_axis_metric')
    with col_t2:
        y_axis = st.selectbox("Select Y-axis metric", [x for x in data_vars if x != x_axis], key='y_axis_metric')
    try:
        st.plotly_chart(
            plot_scatter(dataset=data_filtered, x_col=x_axis, y_col=y_axis, name_col='player_name', value_col='value',
                         color_col='age'))
        st.dataframe(data_filtered[['player_name','season_name',"team_name",'birth_date','age']+[x_axis,y_axis]])
    except:
        st.write("X- and Y-axis not properly defined.")

with tab2:
    st.write(f'Model for {selected_position} contains info on {nsamples} players.\nRsq is {round(r2, 3)}.')
    data_filtered_model = data_filtered[['player_name','season_name','team_name','age','value']+model_features]
    st.dataframe(data_filtered_model)

