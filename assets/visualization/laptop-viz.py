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
)
st.set_option('deprecation.showPyplotGlobalUse', False)

# st.markdown(f"<html style='scroll-behavior: smooth;'></html>", unsafe_allow_html=True)
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

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
# Sections
- [Descriptive Statistic](#descriptive-statistic)
- [Metric](#metric)
''', unsafe_allow_html=True)

st.header("METRIC")

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


st.write("")
st.header("Descriptive Statistic")
# st.markdown("## Descriptive Statistic")
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

st.header('Distribution Data')
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

# PRICEY
def scatter_price_laptop(count, title, asc):
    price_by_laptop = laptop.sort_values('price', ascending=False, ignore_index=True)
    if(asc == "asc"):
        clean_price_laptop = price_by_laptop.head(count)
    elif(asc =="desc"):
        clean_price_laptop = price_by_laptop.tail(count)

    fig = px.scatter(
        data_frame=clean_price_laptop,
        x=clean_price_laptop['brand'],
        y=clean_price_laptop['price'],
        title=title,
        color=clean_price_laptop['brand'],
        hover_name=clean_price_laptop['brand'],
        hover_data=clean_price_laptop,
        symbol=clean_price_laptop['brand'],
        size=clean_price_laptop['price']
    )
    st.plotly_chart(fig, use_container_width=True)

st.header("Best Pricy Laptop 2022")
price_one, price_two = st.columns(2)

with price_one:
    # 10 laptop termahal
    scatter_price_laptop(10, "Top 10 Expensive Laptop", asc="asc")

    # 10 laptop termurah
with price_two:
    scatter_price_laptop(10, "Top 10 Cheap Laptop", asc="desc")

# RATINGS

st.header("Best Rating Laptop 2022")

rating_col_1, rating_col_2 = st.columns([3,9])
with rating_col_1:
    st.write("\n")
    st.write("Insert amount")
    color = st.select_slider(
        'Atur jumlah data yang akan ditampilkan',
        options=[5, 10, 15, 20, 25, 30, 40, 50], key="rating_1")
    st.write(f"Best {color} \n Laptop Ratings")
with rating_col_2:
    rating_5, rating_4, rating_3, rating_2, rating_1 = st.tabs(["Rating :five:", "Rating :four:", "Rating :three:", "Rating :two:", "Rating :one:"])

# FUNC DOT PLOTS RATING
def dot_plots_rating_laptop(rating, bestnum):
    rating_filtered = laptop.loc[(laptop['rating']==rating)]
    sort_rating_price = rating_filtered.sort_values("price", ascending=False)
    data_rating = sort_rating_price.head(bestnum)
    fig = px.scatter(data_rating, y="brand", x="price", color="brand", symbol="brand", hover_data=rating_filtered)
    fig.update_traces(marker_size=10)
    st.plotly_chart(fig, use_container_width=True)

with rating_5:
    dot_plots_rating_laptop(rating=5, bestnum=color)

with rating_4:
    dot_plots_rating_laptop(rating=4, bestnum=color)

with rating_3:
    dot_plots_rating_laptop(rating=3, bestnum=color)

with rating_2:
    dot_plots_rating_laptop(rating=2, bestnum=color)

with rating_1:
    dot_plots_rating_laptop(rating=1, bestnum=color)


# FUNC PIE CHART
def pie_chart(columns, by, values, labels, names, color, title):
    fig = px.pie(laptop.loc[(laptop[columns] == by)], values=values,labels=labels, names=names, color=color, title=f"{title}")

    fig.update_layout(
        xaxis_title=option,
        yaxis_title="Count of " + option)
    st.plotly_chart(fig, use_container_width=True)

# FUNC BAR CHART
def bar_chart(by, columns, return1, return2, title):
    value_counts = laptop[laptop[by] == option][columns].value_counts().reset_index()

    value_counts.columns = [return1, return2]

    fig = px.bar(
        value_counts,
        x=value_counts.columns[0],
        y=value_counts.columns[1],
        text=value_counts.columns[1],
        color=value_counts.columns[0],
        title=f"{title}")

    fig.update_layout(
        xaxis_title=value_counts.columns[0],
        yaxis_title="Count of " + value_counts.columns[0])

    st.plotly_chart(fig, use_container_width=True)

# RAM ORDER
st.header("Distribution Manufacturer Ram by Brand")

# FUNC SELECT BOX CUSTOM
def select_box(title, column, key):
    data = st.selectbox(title, laptop[column].unique(), key=key)
    return data

#
option = select_box(title="Choose a column to plot count. Try Selecting Brand ", column="brand", key="ram")

ram_pie_1, ram_pie_2 = st.columns([6,6])

with ram_pie_1:
    pie_chart(
        columns="brand",
        by=option,
        values="ram_gb",
        labels="ram_gb",
        names="ram_gb",
        color="ram_gb",
        title=f"Distribution of Ram Size Usage by Brand {option}")

with ram_pie_2:
    bar_chart(
        by="brand",
        columns="ram_type",
        return1="Ram Type",
        return2="Count",
        title=f"Distribution of Ram Type Usage by Brand {option}")

# PROCESSOR ORDER
st.header("Distribution Manufacturer Processor by Brand")

option = select_box(title="Choose a column to plot count. Try Selecting Brand ", column="brand", key="procie")
procie_1, procie_2 = st.columns([6,6])

with procie_1:
    # procie_type_count = laptop.groupby('brand')['processor_brand'].value_counts()
    procie_value_count = laptop[laptop['brand'] == option]['processor_brand'].value_counts().reset_index()

    fig = px.scatter(procie_value_count, x="processor_brand", y="count",
                 size="count", color="processor_brand",
                 hover_name="processor_brand", title=f"Distribution of Ram Type Usage \nby Brand {option}",)

    fig.update_layout(
        xaxis_title="Processor Brand",
        yaxis_title="Count of Processor Brand")

    st.plotly_chart(fig, use_container_width=True)



with procie_2:
    bar_chart(
        by="brand",
        columns="processor_gnrtn",
        return1="Processor Generation",
        return2="Count",
        title=f"Distribution of Processor Generation Usage \nby Brand {option}")

# single line
bar_chart(
    by="brand",
    columns="processor_name",
    return1="Processor Name",
    return2="Count",
    title=f"Distribution of Processor Name Usage \nby Brand {option}")







#%%
