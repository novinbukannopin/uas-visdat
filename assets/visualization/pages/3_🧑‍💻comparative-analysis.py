import time  #

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np  # import np
import pandas as pd  # import pd
import plotly.express as px  # import chart
import plotly.graph_objects as go
import streamlit as st
import altair as alt
import math
from PIL import Image

import seaborn as sns
from pandas import DataFrame

st.set_page_config(
    page_title="Real-Time Data Laptop Pricing",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown(f"<html style='scroll-behavior: smooth;'></html>", unsafe_allow_html=True)
# with open('style.css')as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

dataset_url = "https://raw.githubusercontent.com/novinbukannopin/uas-visdat/main/assets/clean/laptop-price.csv"

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

laptop = get_data()

st.subheader("Comparative Analysis") #comparative visualization
column_count_plot = st.selectbox("Choose a column to plot count. Try Selecting Brand ", laptop.columns)
# colname = column_count_plot
value_counts = laptop[column_count_plot].value_counts().reset_index()
value_counts.columns = ['Data', 'Count']
# st.table(value_counts)
fig = px.bar(
    value_counts,
    x='Data',
    y='Count',
    text='Count',
    color='Data',
    title="Bar Chart")

fig.update_layout(
    xaxis_title=column_count_plot,
    yaxis_title="Count of " + column_count_plot)

st.plotly_chart(fig, use_container_width=True)