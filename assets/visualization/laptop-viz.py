import time  #

import matplotlib.pyplot as plt
import numpy as np  # import np
import pandas as pd  # import pd
import plotly.express as px  # import chart
import streamlit as st
import seaborn as sns

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


if st.checkbox("Count Plots"):
    st.subheader("Count Plot")
    column_count_plot = st.selectbox("Choose a column to plot count. Try Selecting Brand ",laptop.columns)
    hue_opt = st.selectbox("Optional categorical variables (countplot hue). Try Selecting Species ",laptop.columns.insert(0,None))
    # if st.checkbox('Plot Countplot'):
    fig = sns.countplot(x=column_count_plot,data=laptop,hue=hue_opt)
    st.pyplot()

if st.checkbox('Histogram | Distplot'):
        st.subheader('Histogram | Distplot')
        st.info("If error, please adjust column name on side panel.")
#         # if st.checkbox('Dist plot'):
        column_dist_plot = st.selectbox("Optional categorical variables (countplot hue). Try Selecting Body Mass",laptop.columns)
        fig = sns.histplot(x = laptop[column_dist_plot])
        # ax = laptop[column_dist_plot].value_counts().plot(kind="bar", colormap="plasma")
        # plt.bar_label(ax.containers[0])
        # plt.ylabel("Counts")
        # plt.xlabel("Brand")
        # plt.title("Counts Laptop by Brand")
#         # fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
        st.pyplot()


# st.title('Create Own Visualization')
# st.markdown("Tick the box on the side panel to create your own Visualization.")
# st.sidebar.subheader('Create Own Visualization')
# if st.sidebar.checkbox('Graphics'):
#     if st.sidebar.checkbox('Count Plot'):
#         st.subheader('Count Plot')
#         st.info("If error, please adjust column name on side panel.")
#         column_count_plot = st.sidebar.selectbox("Choose a column to plot count. Try Selecting Brand ",df.columns)
#         hue_opt = st.sidebar.selectbox("Optional categorical variables (countplot hue). Try Selecting Species ",df.columns.insert(0,None))
#         # if st.checkbox('Plot Countplot'):
#         fig = sns.countplot(x=column_count_plot,data=laptop,hue=hue_opt)
#         st.pyplot()
#
#     if st.sidebar.checkbox('Histogram | Distplot'):
#         st.subheader('Histogram | Distplot')
#         st.info("If error, please adjust column name on side panel.")
#         # if st.checkbox('Dist plot'):
#         column_dist_plot = st.sidebar.selectbox("Optional categorical variables (countplot hue). Try Selecting Body Mass",df.columns)
#         # fig = sns.histplot(x = laptop[column_dist_plot])
#         ax = laptop[column_dist_plot].value_counts().plot(kind="bar", colormap="plasma")
#         plt.bar_label(ax.containers[0])
#         plt.ylabel("Counts")
#         plt.xlabel("Brand")
#         plt.title("Counts Laptop by Brand")
#         # fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
#         st.pyplot()
#
#     if st.sidebar.checkbox('Boxplot'):
#         st.subheader('Boxplot')
#         st.info("If error, please adjust column name on side panel.")
#         column_box_plot_X = st.sidebar.selectbox("X (Choose a column). Try Selecting island:",df.columns.insert(0,None))
#         column_box_plot_Y = st.sidebar.selectbox("Y (Choose a column - only numerical). Try Selecting Body Mass",df.columns)
#         hue_box_opt = st.sidebar.selectbox("Optional categorical variables (boxplot hue)",df.columns.insert(0,None))
#         # if st.checkbox('Plot Boxplot'):
#         fig = sns.boxplot(x=column_box_plot_X, y=column_box_plot_Y,data=laptop,palette="Set3")
#         st.pyplot()

