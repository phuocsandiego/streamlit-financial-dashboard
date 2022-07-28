# Phuoc's Financial Dashboard - Investments Page
# Created: July 22, 2022
# Last Updated: July 26, 2022
# Version: 1.1
# Changes:
# v1.0 - added multi-page support
# v1.1 - separated asset allocation and sector allocation into tabs

import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Investments",
	page_icon=":chart_with_upwards_trend:",
	layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set up some date variables for later use
currentDate = datetime.date.today()
curr_year = currentDate.year
curr_month = currentDate.month

# Read in data from Excel
data_df = pd.read_excel(io="Phuoc-Financial-Data.xlsx", sheet_name="data", skiprows=0)

# METRICS
total_investments = data_df.iloc[5,1]
ytd_earnings = data_df.iloc[68,1]
ytd_contributions = data_df.iloc[65,1]
ytd_portfolio_performance = round(data_df.iloc[67,1]*100,2)
ytd_dividends = data_df.iloc[66,1]

# PORTFOLIO ALLOCATIONS & HOLDINGS TREEMAP CHART DATAFRAMES
asset_allocation = data_df.iloc[54:61]
asset_allocation.columns = ["Asset", "Amount"]
sector_allocation = data_df.iloc[69:79]
sector_allocation.columns = ["Sector", "Amount"]
holdings = data_df.iloc[79:104]
holdings.columns = ["Investment", "Amount"]

# BROKERS AND ACCOUNTS DATAFRAMES
brokers_df = data_df.iloc[44:48]
brokers_df.columns = ["Broker", "Amount"]
accounts_df = data_df.iloc[48:54]
accounts_df.columns = ["Account", "Amount"]

# ---- SIDEBAR ----
# ---- SIDEBAR ----

# ---- MAINPAGE ----
st.title(":chart_with_upwards_trend: Investments")
st.markdown("##")

column_1, column_2, column_3, column_4, column_5 = st.columns(5)
with column_1:
    st.subheader("Portfolio Value")
    st.metric("", "${:,.2f}".format(total_investments))
with column_2:
    st.subheader("Gain/Loss")
    st.metric("", "${:,.2f}".format(ytd_earnings))
with column_3:
    st.subheader("YTD Performance")
    st.metric("", "{}%".format(ytd_portfolio_performance))
with column_4:
    st.subheader("Contributions")
    st.metric("", "${:,.2f}".format(ytd_contributions))
with column_5:
    st.subheader("Dividends")
    st.metric("", "${:,.2f}".format(ytd_dividends))

st.markdown("##")

allocation_tab1, allocation_tab2 = st.tabs(["Asset Allocation", "Sector Allocation"])

with allocation_tab1:
    st.subheader("Asset Allocation")
    # ASSET ALLOCATION [TREEMAP CHART]
    fig_asset_allocation = px.treemap(asset_allocation, path=["Asset"],
                     values="Amount",title="")
    fig_asset_allocation.data[0].textinfo = "label+text+value+percent root"

    fig_asset_allocation.update_layout(margin=dict(l=0,r=0,t=0,b=0))

    st.plotly_chart(fig_asset_allocation, use_container_width=True)

with allocation_tab2:
    st.subheader("Sector Allocation")
    # SECTOR ALLOCATION [TREEMAP CHART]
    fig_sector_allocation = px.treemap(sector_allocation, path=["Sector"],
                     values="Amount",title="")
    fig_sector_allocation.data[0].textinfo = "label+text+value+percent root"

    fig_sector_allocation.update_layout(margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_sector_allocation, use_container_width=True)

# BROKERAGE FIRMS & ACCOUNTS
# BROKER PIE CHART
fig_brokers = px.pie(brokers_df,
    title = "Brokerage Firms",
    names = "Broker",
    values = "Amount",
)
fig_brokers.update_layout(margin=dict(l=0,r=0,t=25,b=0))

# ACCOUNT PIE CHART
fig_accounts = px.pie(accounts_df,
    title = "Accounts",
    names = "Account",
    values = "Amount",
)
fig_accounts.update_layout(margin=dict(l=0,r=0,t=25,b=0))

st.subheader("Brokerage Firms & Accounts")
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_brokers, use_container_width=True)
right_column.plotly_chart(fig_accounts, use_container_width=True)

# HOLDINGS
# HOLDINGS [TREEMAP CHART]
fig_holdings = px.treemap(holdings, path=["Investment"],
                 values="Amount",title="")
fig_holdings.data[0].textinfo = "label+text+value+percent root"

fig_holdings.update_layout(margin=dict(l=0,r=0,t=0,b=0))

st.subheader("Portfolio Holdings")
st.plotly_chart(fig_holdings, use_container_width=True)

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
