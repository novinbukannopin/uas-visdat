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
    initial_sidebar_state="collapsed",
)

st.set_option("deprecation.showPyplotGlobalUse", False)

st.markdown(f"<html style='scroll-behavior: smooth;'></html>", unsafe_allow_html=True)
# with open('style.css')as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

dataset_url = "https://raw.githubusercontent.com/novinbukannopin/uas-visdat/main/assets/clean/laptop-price.csv"


@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)


laptop = get_data()

# st.sidebar.image("../images/laptop-1.jpg")
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.markdown(
    """
> Sections Introduction
1. [Top Priced Laptops by Brand in 2022](#top-priced-laptops-by-brand-in-2022)
2. [Best Rated Laptops in 2022](#best-rated-laptops-in-2022)
3. [Distribution of RAM by Manufacturer and Brand](#distribution-of-ram-by-manufacturer-and-brand)
4. [Distribution of Processors by Manufacturer and Brand](#distribution-of-processors-by-manufacturer-and-brand)
5. [Distribution of Operating Systems](#distribution-of-operating-systems)
6. [Percentage of Laptops with SSD and HDD](#percentage-of-laptops-with-ssd-and-hdd)
7. [Brand-based Weight Graph](#brand-based-weight-graph)
8. [Brand-based Warranty Graph](#brand-based-warranty-graph)
9. [Touchscreen Laptop Graph](#touchscreen-laptop-graph)
10. [MS Office-enabled Laptop Graph](#ms-office-enabled-laptop-graph)
""",
    unsafe_allow_html=True,
)

# Persebaran Sistem Operasi
# Grafik Berat Laptop Berdasarkan Brand
# Grafik Laptop Touchscreen
# Grafik Laptop Yang Mendapatkan MS Office


# PRICEY
def scatter_price_laptop(count, title, asc):
    price_by_laptop = laptop.sort_values("price", ascending=False, ignore_index=True)
    if asc == "asc":
        clean_price_laptop = price_by_laptop.head(count)
    elif asc == "desc":
        clean_price_laptop = price_by_laptop.tail(count)

    fig = px.scatter(
        data_frame=clean_price_laptop,
        x=clean_price_laptop["brand"],
        y=clean_price_laptop["price"],
        title=title,
        color=clean_price_laptop["brand"],
        hover_name=clean_price_laptop["brand"],
        hover_data=clean_price_laptop,
        symbol=clean_price_laptop["brand"],
        size=clean_price_laptop["price"],
    )
    st.plotly_chart(fig, use_container_width=True)


st.header("Top Priced Laptops by Brand in 2022")
price_one, price_two = st.columns(2)

with price_one:
    # 10 laptop termahal
    scatter_price_laptop(10, "Top 10 Most Expensive Laptops", asc="asc")

    # 10 laptop termurah
with price_two:
    scatter_price_laptop(10, "Top 10 Affordable Laptops", asc="desc")

# RATINGS

st.header("Best Rated Laptops in 2022")

rating_col_1, rating_col_2 = st.columns([3, 9])
with rating_col_1:
    st.write("\n")
    st.write("Insert amount")
    color = st.select_slider(
        "Set the number of data to be displayed",
        options=[5, 10, 15, 20, 25, 30, 40, 50],
        key="rating_1",
    )
    st.write(f"Top {color} \n Laptop Ratings")
with rating_col_2:
    rating_5, rating_4, rating_3, rating_2, rating_1 = st.tabs(
        [
            "Rating :five:",
            "Rating :four:",
            "Rating :three:",
            "Rating :two:",
            "Rating :one:",
        ]
    )


# FUNC DOT PLOTS RATING
def dot_plots_rating_laptop(rating, bestnum):
    rating_filtered = laptop.loc[(laptop["rating"] == rating)]
    sort_rating_price = rating_filtered.sort_values("price", ascending=False)
    data_rating = sort_rating_price.head(bestnum)
    fig = px.scatter(
        data_rating,
        y="brand",
        x="price",
        color="brand",
        symbol="brand",
        hover_data=rating_filtered,
    )
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
    fig = px.pie(
        laptop.loc[(laptop[columns] == by)],
        values=values,
        labels=labels,
        names=names,
        color=color,
        title=f"{title}",
    )

    fig.update_layout(xaxis_title=option, yaxis_title="Count of " + option)
    st.plotly_chart(fig, use_container_width=True)


# FUNC BAR CHART
def bar_chart(by, columns, return1, return2, title, orientation):
    value_counts = laptop[laptop[by] == option][columns].value_counts().reset_index()

    value_counts.columns = [return1, return2]

    fig = px.bar(
        value_counts,
        x=value_counts.columns[0],
        y=value_counts.columns[1],
        text=value_counts.columns[1],
        color=value_counts.columns[0],
        title=f"{title}",
        orientation=orientation,
    )

    fig.update_layout(
        xaxis_title=value_counts.columns[0],
        yaxis_title="Count of " + value_counts.columns[0],
    )

    st.plotly_chart(fig, use_container_width=True)


# RAM ORDER
st.header(
    "Distribution of RAM by Manufacturer and Brand"
)  # RAM Distribution by Manufacturer Brand,RAM Distribution by Brand


# FUNC SELECT BOX CUSTOM
def select_box(title, column, key):
    data = st.selectbox(title, laptop[column].unique(), key=key)
    return data


#
option = select_box(
    title="Choose a column to plot count. Try Selecting Brand ",
    column="brand",
    key="ram",
)

ram_pie_1, ram_pie_2 = st.columns([6, 6])

with ram_pie_1:
    pie_chart(
        columns="brand",
        by=option,
        values="ram_gb",
        labels="ram_gb",
        names="ram_gb",
        color="ram_gb",
        title=f"Distribution of RAM Size Usage by {option} Brand ",
    )

with ram_pie_2:
    bar_chart(
        by="brand",
        columns="ram_type",
        return1="Ram Type",
        return2="Count",
        title=f"Distribution of RAM Type Usage by {option} Brand ",
        orientation="v",
    )

# PROCESSOR ORDER
st.header(
    "Distribution of Processors by Manufacturer and Brand"
)  # Processor Distribution by Manufacturer and Brand, Processor Distribution by Manufacturer and Brand.

option = select_box(
    title="Choose a column to plot count. Try Selecting Brand ",
    column="brand",
    key="procie",
)
procie_1, procie_2 = st.columns([6, 6])

with procie_1:
    # procie_type_count = laptop.groupby('brand')['processor_brand'].value_counts()
    procie_value_count = (
        laptop[laptop["brand"] == option]["processor_brand"]
        .value_counts()
        .reset_index()
    )

    fig = px.scatter(
        procie_value_count,
        x="processor_brand",
        y="count",
        size="count",
        color="processor_brand",
        hover_name="processor_brand",
        title=f"Distribution of Processor Brand \nby {option} Brand",
    )

    fig.update_layout(
        xaxis_title="Processor Brand", yaxis_title="Count of Processor Brand"
    )

    st.plotly_chart(fig, use_container_width=True)


with procie_2:
    bar_chart(
        by="brand",
        columns="processor_gnrtn",
        return1="Processor Generation",
        return2="Count",
        title=f"Distribution of Processor Generation Usage \nby {option} Brand",
        orientation="v",
    )

# single line
bar_chart(
    by="brand",
    columns="processor_name",
    return1="Processor Name",
    return2="Count",
    title=f"Distribution of Processor Name Usage \nby {option} Brand",
    orientation="v",
)


#
# Tentu! Berikut beberapa rekomendasi judul untuk chart yang dapat ditampilkan di dashboard berdasarkan data laptop yang Anda berikan:
#
# Perbandingan Harga Laptop Berdasarkan Brand
# Distribusi Prosesor Berdasarkan Brand
# Grafik Jenis RAM yang Digunakan pada Laptop
# Persentase Laptop dengan SSD dan HDD
# Penyebaran Sistem Operasi pada Laptop
# Rasio Laptop dengan Grafik Kard Terintegrasi dan Diskret
# Grafik Berat Laptop Berdasarkan Brand
# Durasi Garansi Laptop pada Berbagai Brand
# Persentase Laptop dengan Layar Sentuh
# Pemakaian Microsoft Office pada Laptop

# ssd hdd

st.header("Percentage of Laptops with SSD and HDD")  #

option = select_box(
    title="Choose a column to plot count. Try Selecting Brand ",
    column="brand",
    key="ssd_hdd",
)
ssd, hdd = st.columns([6, 6])

with ssd:
    pie_chart(
        columns="brand",
        by=option,
        values="ssd",
        labels="ssd",
        names="ssd",
        color="ssd",
        title=f"Distribution of SSD Storage by {option} Brand ",
    )

with hdd:
    pie_chart(
        columns="brand",
        by=option,
        values="hdd",
        labels="hdd",
        names="hdd",
        color="hdd",
        title=f"Distribution of HDD Storage by {option} Brand ",
    )

# ssd hdd
st.header("Distribution of Operating Systems")  #

os, os_bit = st.columns([5, 7])
with os:
    os = laptop.groupby(["brand", "os", "os_bit"]).size().reset_index(name="count")
    fig = px.bar(
        os,
        x="brand",
        y="count",
        color="os",
        barmode="group",
        title="\n Data Distribution Chart",
    )  # semua
    st.plotly_chart(fig, use_container_width=True)

with os_bit:
    option = select_box(
        title="Choose a column to plot count. Try Selecting ASUS ",
        column="brand",
        key="os",
    )
    option_laptop = laptop.loc[laptop["brand"] == option]
    os_brand, os_bit_brand = st.columns([6, 6])
    with os_brand:
        os = (
            option_laptop.groupby(["brand", "os", "os_bit"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(os, x="brand", y="count", color="os_bit", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    with os_bit_brand:
        os = (
            option_laptop.groupby(["brand", "os", "os_bit"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(os, x="brand", y="count", color="os", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

# weight
st.header("Brand-based Weight Graph")  # Brand-based Weight Chart
os = laptop.groupby(["weight", "brand"]).size().reset_index(name="count")
fig = px.bar(
    os,
    x="brand",
    y="count",
    color="weight",
    barmode="group",
    title="\n Data Distribution Chart",
)  # semua
st.plotly_chart(fig, use_container_width=True)
# warranty
st.header("Brand-based Warranty Graph")
os = laptop.groupby(["warranty", "brand"]).size().reset_index(name="count")
fig = px.bar(
    os,
    x="brand",
    y="count",
    color="warranty",
    title="\n Data Distribution Chart for a Specific Year",
)  # yearly data distribution
st.plotly_chart(fig, use_container_width=True)


# touchscreen
st.header("Touchscreen Laptop Graph")

touchscreen_counts = (
    laptop[laptop["touchscreen"] == True]["brand"].value_counts().reset_index()
)
touchscreen_counts.columns = ["brand", "touchscreen_count"]

non_touchscreen_counts = (
    laptop[laptop["touchscreen"] == False]["brand"].value_counts().reset_index()
)
non_touchscreen_counts.columns = ["brand", "non_touchscreen_count"]

merged_counts = touchscreen_counts.merge(
    non_touchscreen_counts, on="brand", how="outer"
)
merged_counts = merged_counts.fillna(0)

total_counts = (
    merged_counts["touchscreen_count"] + merged_counts["non_touchscreen_count"]
)
merged_counts["touchscreen_percentage"] = (
    merged_counts["touchscreen_count"] / total_counts
) * 100
merged_counts["non_touchscreen_percentage"] = (
    merged_counts["non_touchscreen_count"] / total_counts
) * 100

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=merged_counts["brand"],
        y=merged_counts["touchscreen_count"],
        name="Touchscreen",
        textposition="auto",
        hovertemplate="Brand: %{x}<br>Touchscreen Count: %{y}",
    )
)

fig.add_trace(
    go.Bar(
        x=merged_counts["brand"],
        y=merged_counts["non_touchscreen_count"],
        name="Non-Touchscreen",
        textposition="auto",
        hovertemplate="Brand: %{x}<br>Non-Touchscreen Count: %{y}",
    )
)

fig.update_layout(
    barmode="stack",
    title="Touchscreen vs Non-Touchscreen Laptops by Brand",
    xaxis_title="Brand",
    yaxis_title="Count",
)

st.plotly_chart(fig, use_container_width=True)

# Office
st.header("MS Office-enabled Laptop Graph")

msoffice_counts = (
    laptop[laptop["msoffice"] == True]["brand"].value_counts().reset_index()
)
msoffice_counts.columns = ["brand", "msoffice_count"]

non_msoffice_counts = (
    laptop[laptop["msoffice"] == False]["brand"].value_counts().reset_index()
)
non_msoffice_counts.columns = ["brand", "non_msoffice_count"]

merged_counts = msoffice_counts.merge(non_msoffice_counts, on="brand", how="outer")
merged_counts = merged_counts.fillna(0)

total_counts = merged_counts["msoffice_count"] + merged_counts["non_msoffice_count"]
merged_counts["msoffice_percentage"] = (
    merged_counts["msoffice_count"] / total_counts
) * 100
merged_counts["non_msoffice_percentage"] = (
    merged_counts["non_msoffice_count"] / total_counts
) * 100

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=merged_counts["brand"],
        y=merged_counts["msoffice_count"],
        name="Touchscreen",
        textposition="auto",
        hovertemplate="Brand: %{x}<br>Touchscreen Count: %{y}",
    )
)

fig.add_trace(
    go.Bar(
        x=merged_counts["brand"],
        y=merged_counts["non_msoffice_count"],
        name="Non-Touchscreen",
        textposition="auto",
        hovertemplate="Brand: %{x}<br>Non-Touchscreen Count: %{y}",
    )
)

fig.update_layout(
    barmode="stack",
    title="Distribution Included Microsoft Office Laptops by Brand",
    xaxis_title="Brand",
    yaxis_title="Count",
)

st.plotly_chart(fig, use_container_width=True)


# %%
