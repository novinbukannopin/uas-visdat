import time  #

import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
import numpy as np  # import np
import pandas as pd  # import pd
import plotly.express as px  # import chart
import streamlit as st
import altair as alt

import seaborn as sns
from pandas import DataFrame


st.set_page_config(
    page_title="Real-Time Data Laptop Pricing",
    page_icon="✅",
    layout="wide",
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


st.markdown("## Descriptive Statistic")
st.write("")

#
def kpi(subheader, label, option_columns, method):
    st.subheader(subheader)
    if option_columns == "all":
        hue_opt = st.selectbox(label=label, options=laptop.columns)
    else:
        hue_opt = st.selectbox(label=label, options=option_columns)

    column = hue_opt.lower()
    title = hue_opt.replace("_", " ").upper()
    st.markdown(f"<h4 style='text-align: center; color: #6554AF;'>{title}</h3>", unsafe_allow_html=True)
    count = laptop[column].nunique()
    if count != None:
        st.markdown(f"<h1 style='text-align: center; color: #9575DE;'>{count} item</h1>", unsafe_allow_html=True)
        if method == "counts":
            st.table(laptop[column].value_counts())
        elif method == "mean":
            st.table(laptop[column].groupby(laptop['brand']).mean())
        elif method == "range":
            min_value = laptop[column].groupby(laptop['brand']).min()
            max_value = laptop[column].groupby(laptop['brand']).max()
            range = max_value - min_value
            st.table(
                {"range": range, "min": min_value, "max": max_value}
            )

kpi_count, kpi_mean, kpi_range = st.columns(3)
with kpi_count:
    kpi(
        subheader=":department_store: This is a Count Item",
        label="count",
        option_columns="all",
        method="counts")

with kpi_mean:
    kpi(
        subheader=":snowman: This is Average",
        label="mean",
        option_columns=(['price', 'rating']),
        method="mean")

with kpi_range:
    kpi(
        subheader=":snowman: This is Range",
        label="range",
        option_columns=(['price', 'rating']),
        method="range")


st.markdown("<hr/>",unsafe_allow_html=True)

st.markdown("## Visualization Data")
st.write("")

cccount, col2 = st.columns(2)
# with cccount:
colname = ""
st.subheader("Comparison of amounts ")
column_count_plot = st.selectbox("Choose a column to plot count. Try Selecting Brand ",laptop.columns)
colname = column_count_plot
value_counts = laptop[column_count_plot].value_counts().reset_index()
value_counts.columns = ['Data', 'Count']

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

# with col2:
st.subheader('Distribution Data')
option_columns = ["warranty", "msoffice", "os", "windows", "weight", "touchscreen"]
option_columns_num = [
    "brand", "processor_brand",
    "processor_name", "processor_gnrtn",
    "ram_type", "ram_gb",
    'ssd', 'hdd']

choice_categorical = st.selectbox("Choose the enabled variable used for the x-axis. Try Selecting Warranty", options=option_columns)

choice_categorical_num = st.selectbox("Choose the enabled variable used for the legend. Try Selecting Brand", options=option_columns_num)

value_counts = laptop[choice_categorical_num]\
    .groupby(laptop[choice_categorical])\
    .value_counts()\
    .reset_index()

value_counts.columns = ['Data', choice_categorical_num, 'Count']

fig = px.histogram(
    value_counts,
    x="Data",
    y="Count",
    color=choice_categorical_num,
    title="Histogram of " +choice_categorical)

st.plotly_chart(fig, use_container_width=True)

# 10 laptop termahal
rich_laptop = laptop.sort_values('price', ascending=False, ignore_index=True)

ten_laptop = rich_laptop.head(10)


fig = px.scatter(
    data_frame=ten_laptop, x=ten_laptop['brand'], y=ten_laptop['price'], title="10 Laptop yang Expensive", color=ten_laptop['brand'], hover_data=ten_laptop, symbol=ten_laptop['brand']
)
st.plotly_chart(fig, use_container_width=True)

# 10 laptop termurah
rich_laptop = laptop.sort_values('price', ascending=False, ignore_index=True)

ten_laptop_murah = rich_laptop.tail(10)


fig = px.scatter(
    data_frame=ten_laptop_murah, x=ten_laptop_murah['brand'], y=ten_laptop_murah['price'], title="10 Laptop yang Cheap", color=ten_laptop_murah['brand'], hover_data=ten_laptop_murah, symbol=ten_laptop_murah['brand']
)
st.plotly_chart(fig, use_container_width=True)

# rating
laptop["total_rating"] = laptop['rating'] * laptop["no_ratings"]
best_rating = laptop.sort_values('total_rating', ascending=False, ignore_index=True)
best_rating_filtered = best_rating[best_rating['rating'] == 5]
st.table(best_rating_filtered.head(10))

