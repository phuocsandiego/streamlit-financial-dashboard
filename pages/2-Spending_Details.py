# Phuoc's Financial Dashboard - Spending Details Page
# Created: July 22, 2022
# Last Updated: July 26, 2022
# Version: 1.1
# Changes:
# v1.0 - added multi-page support
# v1.1 - moved spending details to tabs instead of tables on the main page

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Spending Details",
	page_icon=":dollar:",
	layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

currentDate = datetime.date.today()
curr_year = currentDate.year
curr_month = currentDate.month

spend_data = pd.read_excel(io="Phuoc-Financial-Data.xlsx", sheet_name="spend_data", skiprows=0)

# YTD Budget
monthly_budget = 7850
ytd_budget = monthly_budget*curr_month
ytd_spend = spend_data.loc[spend_data["Year"]==curr_year]
mtd_spend = ytd_spend.loc[ytd_spend["Month"]==curr_month]
mtd_spend_table = mtd_spend.copy()
mtd_spend_table.loc[:, "Amount"] = mtd_spend_table["Amount"].map("${:,.2f}".format)
#mtd_spend_table.Date.apply(lambda x: x.date())

historical_spend_table = spend_data.copy()
historical_spend_table.loc[:, "Amount"] = historical_spend_table["Amount"].map("${:,.2f}".format)

mtd_spend_total = ytd_spend.loc[ytd_spend["Month"]==curr_month]["Amount"].sum()
mtd_spend_variance = (mtd_spend_total-monthly_budget)*(-1)
total_ytd_spend = ytd_spend["Amount"].sum()
ytd_variance = (total_ytd_spend-ytd_budget)*(-1)
ytd_monthly_average_spend = total_ytd_spend/curr_month
ytd_monthly_average_spend_variance = (ytd_monthly_average_spend-monthly_budget)*(-1)

# ---- SIDEBAR ----
st.sidebar.subheader("Historical Spend Filters:")
year = st.sidebar.multiselect(
    "Year:",
    options=spend_data["Year"].unique(),
    default=spend_data["Year"].unique()
)

month = st.sidebar.multiselect(
    "Month:",
    options=spend_data["Month"].unique(),
    default=spend_data["Month"].unique(),
)

category = st.sidebar.multiselect(
    "Category:",
    options=spend_data["Category"].unique(),
    default=spend_data["Category"].unique()
)

df_selection = spend_data.query(
    "Year == @year & Month ==@month & Category == @category"
)
# ---- SIDEBAR ----

# ---- MAINPAGE ----
st.title(":dollar: Spending Details")
st.markdown("##")

# METRICS
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("YTD Spend")
    #st.write("Left Subheader")
    st.metric("", "${:,.2f}".format(total_ytd_spend), "${:,.2f}".format(-ytd_variance))
with middle_column:
    st.subheader("MTD Spend")
    st.metric("", "${:,.2f}".format(mtd_spend_total), "${:,.2f}".format(-mtd_spend_variance))
with right_column:
    st.subheader("Monthly Average")
    st.metric("", "${:,.2f}".format(ytd_monthly_average_spend), "${:,.2f}".format(-ytd_monthly_average_spend_variance))
# METRICS

st.markdown("##")

### CURRENT MONTH SPENDING ###
monthly_tab1, monthly_tab2 = st.tabs(["Current Month Spend", "Current Month Spend Details"])

with monthly_tab1:
    st.subheader("Current Month Spend")
    # CURRENT MONTH SPEND BY CATEGORY [TREEMAP CHART]
    fig_mtd_spend_by_cateogry = px.treemap(mtd_spend, path=["Category"],
                     values="Amount",title="")
    fig_mtd_spend_by_cateogry.data[0].textinfo = "label+text+value+percent root"

    fig_mtd_spend_by_cateogry.update_layout(margin=dict(l=0,r=0,t=0,b=0))

    st.plotly_chart(fig_mtd_spend_by_cateogry, use_container_width=True)
    # CURRENT MONTH SPEND BY CATEGORY [TREEMAP CHART]

with monthly_tab2:
    st.subheader("Current Month Spend Details")
    # ---- MTD SPEND TABLE ----
    fig_monthly_spend_table = go.Figure(data=go.Table(
        header = dict(values=list(mtd_spend_table[["Date", "Account", "Description", "Category","Amount"]].columns),
            font=dict(color='white', size=16),
            line_color="#222222",
            fill_color = "#0083B8",
            align = "left"),
        cells = dict(values=[mtd_spend_table.Date, mtd_spend_table.Account, mtd_spend_table.Description, mtd_spend_table.Category, mtd_spend_table.Amount],
            font=dict(color="#eeeeee", size=14),
            height = 30,
            line_color="#222222",
            fill_color = "#444444",
            align = "left")
            ))
    fig_monthly_spend_table.update_layout(margin=dict(l=0,r=0,t=0,b=0))
    # ---- MTD SPEND TABLE ----

    st.plotly_chart(fig_monthly_spend_table, use_container_width=True)
### CURRENT MONTH SPENDING ###

### CURRENT YEAR SPENDING ###
yearly_tab1, yearly_tab2 = st.tabs(["YTD Monthly Spend", "YTD Spend by Category"])

with yearly_tab1:
    st.subheader("Current Year Spend")
    # SPEND BY MONTH [BAR CHART]
    spend_by_month = ytd_spend.groupby(by=["Month"]).sum()[["Amount"]]
    fig_monthly_spend = px.bar(
        spend_by_month,
        x=spend_by_month.index,
        y="Amount",
        title="",
        color_discrete_sequence=["#0083B8"] * len(spend_by_month),
        template="plotly_white",
    )
    fig_monthly_spend.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_monthly_spend.update_layout(margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_monthly_spend, use_container_width=True)

with yearly_tab2:
    st.subheader("Current Year Spend by Category")
    # SPEND BY CATEGORY [TREEMAP CHART]
    fig_spend_by_cateogry = px.treemap(ytd_spend, path=["Category"],
                     values="Amount",title="")
    fig_spend_by_cateogry.data[0].textinfo = "label+text+value+percent root"
    fig_spend_by_cateogry.update_layout(margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_spend_by_cateogry, use_container_width=True)
### CURRENT YEAR SPENDING ###

### HISTORICAL SPEND ###
historical_tab1, historical_tab2 = st.tabs(["Spend by Year", "Detailed Historical Spend"])

with historical_tab1:
    st.subheader("Spend by Year")
    # SPEND BY YEAR [BAR CHART]
    spend_by_year = df_selection.groupby(by=["Year"]).sum()[["Amount"]]
    fig_yearly_spend = px.bar(
        spend_by_year,
        x=spend_by_year.index,
        y="Amount",
        title="",
        color_discrete_sequence=["#0083B8"] * len(spend_by_year),
        template="plotly_white",
    )
    fig_yearly_spend.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_yearly_spend.update_layout(margin=dict(l=0,r=0,t=0,b=0))

    st.plotly_chart(fig_yearly_spend, use_container_width=True)

with historical_tab2:
    st.subheader("Historical Spend Details")
    # ---- HISTORICAL SPEND TABLE ----
    fig_historical_spend_table = go.Figure(data=go.Table(
        header = dict(values=list(historical_spend_table[["Date", "Account", "Description", "Category","Amount"]].columns),
            font=dict(color='white', size=16),
            line_color="#222222",
            fill_color = "#0083B8",
            align = "left"),
        cells = dict(values=[historical_spend_table.Date, historical_spend_table.Account, historical_spend_table.Description, historical_spend_table.Category, historical_spend_table.Amount],
            font=dict(color="#eeeeee", size=14),
            height = 30,
            line_color="#222222",
            fill_color = "#444444",
            align = "left")
            ))
    fig_historical_spend_table.update_layout(margin=dict(l=0,r=0,t=0,b=0))
    # ---- HISTORICAL SPEND TABLE ----

    st.plotly_chart(fig_historical_spend_table, use_container_width=True)

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