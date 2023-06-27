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

dataset_url = "https://raw.githubusercontent.com/novinbukannopin/uas-visdat/main/assets/clean/laptop-price.csv"

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

laptop = get_data()



st.title("Real-Time / Live Data Laptop Dashboard")

st.markdown('''
        This dataset represents various models of laptops from various brands with features such as brand, processor_brand, processor_name, ram_gb, ram_type, SSD, HDD, os, os_bit, graphic_card_gb, weight, warranty, touch screen, MSOffice, price, rating, Number of Ratings, Number of Reviews. Here, price is an independent variable so this dataset can be used for regression analysis to predict the prices of laptops based on their features.
    ''')

st.sidebar.markdown('''
> Sections Introduction
1. [Metric](#metric)
2. [Table](#table)
''', unsafe_allow_html=True)

st.subheader("Metric")

jumlah_brand = len(laptop['brand'].unique())
processor_name = len(laptop['processor_name'].unique())
processor_brand = len(laptop['processor_brand'].unique())
ram_type = len(laptop['ram_type'].unique())
total_product = len(laptop['brand'])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Product", f"{str(total_product)} Product", "20%")
col2.metric("Brand Laptop", f"{str(jumlah_brand)} Brand", "-8%")
col3.metric("Processor", f"{str(processor_name)} Type", "15%")
col4.metric("Brand Procie", f"{str(processor_brand)} Brand", "5%")
col5.metric("Ram Type", f"{str(jumlah_brand)} Type", "40%")

st.subheader("Table")
st.table(laptop)