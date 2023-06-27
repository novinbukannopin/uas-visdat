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



st.header('Distribution Analysis') #Distribution Visualization
option_columns = ["warranty", "msoffice", "os", "windows", "weight", "touchscreen"]
option_columns_num = [
    "brand", "processor_brand",
    "processor_name", "processor_gnrtn",
    "ram_type", "ram_gb",
    'ssd', 'hdd']

choice_categorical = st.selectbox("Choose the enabled variable used for the x-axis. Try Selecting Warranty", options=option_columns)

choice_categorical_num = st.selectbox("Choose the enabled variable used for the legend. Try Selecting Brand", options=option_columns_num)

value_counts = laptop[choice_categorical_num] \
    .groupby(laptop[choice_categorical]) \
    .value_counts() \
    .reset_index()

value_counts.columns = ['Data', choice_categorical_num, 'Count']

fig = px.histogram(
    value_counts,
    x="Data",
    y="Count",
    color=choice_categorical_num,
    title="Histogram of " +choice_categorical)

st.plotly_chart(fig, use_container_width=True)