# Phuoc's Financial Dashboard
# Created: July 22, 2022
# Last Updated: July 25, 2022
# Version: 1.0
# Changes:
# v1.0 - added multi-page support

import pandas as pd
import plotly.express as px
import streamlit as st
import xlrd

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Phuoc's Financial Dashboard",
	page_icon=":bar_chart:",
	layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

data_df = pd.read_excel(io="Phuoc-Financial-Data.xlsx", sheet_name="data", skiprows=0)
networth = "${:,.2f}".format(data_df.iloc[1,1])
networth_change = data_df.iloc[2,1]*(-1)
retirement_score = "{}%".format(data_df.iloc[15,1])
retirement_date_serial = data_df.iloc[18,1]
net_worth_chart_df = data_df.iloc[range(19, 43, 1),:]
net_worth_chart_df.rename(columns = {list(net_worth_chart_df)[0]: 'Month'}, inplace = True)
net_worth_chart_df.rename(columns = {list(net_worth_chart_df)[1]: 'Net Worth'}, inplace = True)

# NET WORTH CHART
fig_net_worth = px.area(
    net_worth_chart_df["Net Worth"],
    x=net_worth_chart_df.Month,
    y="Net Worth",
    title="",
    color_discrete_sequence=["#0083B8"] * len(net_worth_chart_df),
    template="plotly_white",
)
fig_net_worth.update_layout(
    xaxis=dict(tickmode="linear"),
    xaxis_title="Month",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# Calling the xldate_as_datetime() function to
# convert the specified excel serial date into
# datetime.datetime object
retirement_date = xlrd.xldate_as_datetime(retirement_date_serial, 0)
retirement_date = retirement_date.strftime("%B %d, %Y")

# ---- SIDEBAR ----
# ---- SIDEBAR ----

# ---- MAINPAGE ----
st.title(":bar_chart: Phuoc's Financial Dashboard")
st.markdown("##")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Current Net Worth")
    #st.write("Left Subheader")
    st.metric("", networth, "-${:,.2f}".format(networth_change))
with middle_column:
    st.subheader("Retirement Progress")
    st.metric("", retirement_score)
with right_column:
    st.subheader("Retirement Date")
    st.metric("", retirement_date)

st.markdown("""---""")

st.subheader("Net Worth - Past 24 Months")
st.plotly_chart(fig_net_worth, use_container_width=True)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Assets")
    st.metric("", "${:,.2f}".format(data_df.iloc[3,1]))
with right_column:
    st.subheader("Liabilities")
    st.metric("", "${:,.2f}".format(-data_df.iloc[4,1]))


#st.dataframe(data_df)
#st.dataframe(net_worth_chart_df)

st.markdown("##")
st.markdown("##")
st.write("© Copyright 2022 Phuoc Le.  All rights reserved.")
# ---- MAINPAGE ----

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# ---- HIDE STREAMLIT STYLE ----