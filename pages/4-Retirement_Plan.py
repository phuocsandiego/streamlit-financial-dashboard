# Phuoc's Financial Dashboard - Retirement Plan Page
# Created: July 22, 2022
# Last Updated: July 27, 2022
# Version: 1.1
# Changes:
# v1.0 - added multi-page support
# v1.1 - added Retirement Fund Balance assumptions tab
# v1.1 - added Retirement Asset Allocation

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import xlrd

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Retirement Plan",
	page_icon=":sunny:",
	layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Read in Excel data file
data_df = pd.read_excel(io="Phuoc-Financial-Data.xlsx", sheet_name="data", skiprows=0)

# Set up metrics
total_investments = data_df.iloc[5,1]
networth_change = data_df.iloc[2,1]*(-1)
retirement_score = "{}%".format(data_df.iloc[15,1])
retirement_date_serial = data_df.iloc[18,1]
retirement_value = data_df.iloc[110,1]
monthly_income = data_df.iloc[14,1]

# Calling the xldate_as_datetime() function to
# convert the specified excel serial date into
# datetime.datetime object
retirement_date = xlrd.xldate_as_datetime(retirement_date_serial, 0)
retirement_date = retirement_date.strftime("%B %d, %Y")

# Retirement Fund Growth
retirement_fund = data_df.iloc[range(110, 155, 1),:]
retirement_fund.rename(columns = {list(retirement_fund)[0]: 'Year'}, inplace = True)
retirement_fund.rename(columns = {list(retirement_fund)[1]: 'Amount'}, inplace = True)

# Retirement Fund Assumptions
investment_growth = data_df.iloc[7,1] * 100
inflation = data_df.iloc[107,1] * 100
safe_withdrawal_rate = data_df.iloc[6,1] * 100
social_security_income = data_df.iloc[109,1]
social_security_age = data_df.iloc[108,1] - 1975

gross_annual_income = data_df.iloc[106,1]
net_monthly_income = data_df.iloc[14,1]
net_annual_income = net_monthly_income * 12
income_taxes = gross_annual_income - net_annual_income

assumptions1 = {
  "assumptions": ["Investment Growth Rate:", "Inflation:", "Safe Withdrawal Rate:", "Social Security Income:", "Social Security Age:"],
  "amount": ["{}%".format(investment_growth), "{}%".format(inflation), "{}%".format(safe_withdrawal_rate), "${:,.2f}".format(social_security_income), social_security_age]
}

assumptions1_df = pd.DataFrame(assumptions1)

fig_assumptions1 = go.Figure(data=go.Table(
    cells = dict(values=[assumptions1_df.assumptions, assumptions1_df.amount],
        font=dict(color="#eeeeee", size=18),
        height=30,
        line_color="#222222",
        fill_color = "#444444",
        align = "left")
        ))
fig_assumptions1.layout['template']['data']['table'][0]['header']['fill']['color']='rgba(0,0,0,0)'
fig_assumptions1.layout['template']['data']['table'][0]['header']['line']['color']='rgba(0,0,0,0)'
fig_assumptions1.update_layout(margin=dict(l=0,r=0,t=0,b=0))

assumptions2 = {
  "assumptions": ["Gross Annual Income:", "Federal & State Income Taxes:", "Net Annual Income:", "Net Monthly Income:"],
  "amount": ["${:,.2f}".format(gross_annual_income), "${:,.2f}".format(income_taxes), "${:,.2f}".format(net_annual_income), "${:,.2f}".format(net_monthly_income)]
}

assumptions2_df = pd.DataFrame(assumptions2)

fig_assumptions2 = go.Figure(data=go.Table(
    cells = dict(values=[assumptions2_df.assumptions, assumptions2_df.amount],
        font=dict(color="#eeeeee", size=18),
        height=30,
        line_color="#222222",
        fill_color = "#444444",
        align = "left")
        ))
fig_assumptions2.layout['template']['data']['table'][0]['header']['fill']['color']='rgba(0,0,0,0)'
fig_assumptions2.layout['template']['data']['table'][0]['header']['line']['color']='rgba(0,0,0,0)'
fig_assumptions2.update_layout(margin=dict(l=0,r=0,t=0,b=0))
# Retirement Fund Assumptions

# Retirement Budget
retirement_budget = data_df.iloc[range(155, 164, 1),:]
retirement_budget.rename(columns = {list(retirement_budget)[0]: 'Category'}, inplace = True)
retirement_budget.rename(columns = {list(retirement_budget)[1]: 'Amount'}, inplace = True)
# Retirement Budget

# Retirement Portfolio Allocation
retirement_allocation = data_df.iloc[range(164, 169, 1),:]
retirement_allocation.rename(columns = {list(retirement_allocation)[0]: 'Asset Class'}, inplace = True)
retirement_allocation.rename(columns = {list(retirement_allocation)[1]: 'Percentage'}, inplace = True)
# Retirement Portfolio Allocation

# ---- SIDEBAR ----
# ---- SIDEBAR ----

# ---- MAINPAGE ----
st.title(":sunny: Retirement Plan")
st.markdown("##")

column_1, column_2, column_3, column_4, column_5 = st.columns(5)
with column_1:
    st.subheader("Current Value")
    #st.write("Left Subheader")
    st.metric("", "${:,.2f}".format(total_investments))
with column_2:
    st.subheader("Retirement Value")
    st.metric("", "${:,.2f}".format(retirement_value))
with column_3:
    st.subheader("Progress")
    st.metric("", retirement_score)
with column_4:
    st.subheader("Monthly Income")
    st.metric("", "${:,.2f}".format(monthly_income))
with column_5:
    st.subheader("Retirement Date")
    st.metric("", retirement_date)

st.markdown("##")

retirement_fund_tab1, retirement_fund_tab2 = st.tabs(["Retirement Fund Balance", "Assumptions"])

with retirement_fund_tab1:
    # RETIREMENT FUND CHART
    st.subheader("Retirement Balance - 45 Years")

    fig_retirement_fund = px.area(
        retirement_fund["Amount"],
        x=retirement_fund.Year,
        y="Amount",
        title="",
        color_discrete_sequence=["#0083B8"] * len(retirement_fund),
        template="plotly_white",
    )
    fig_retirement_fund.update_layout(
        xaxis=dict(tickmode="linear"),
        xaxis_title="Year",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    fig_retirement_fund.update_layout(margin=dict(l=0,r=0,t=0,b=0))

    st.plotly_chart(fig_retirement_fund, use_container_width=True)
    # RETIREMENT FUND CHART

with retirement_fund_tab2:
    column1, column2 = st.columns(2)
    column1.plotly_chart(fig_assumptions1, use_container_width=True)
    column2.plotly_chart(fig_assumptions2, use_container_width=True)

st.markdown("##")

# BUDGET
fig_budget = px.pie(retirement_budget,
    title = "Retirement Budget",
    names = "Category",
    values = "Amount",
)
fig_budget.update_layout(margin=dict(l=0,r=0,t=25,b=0))
# BUDGET

# RETIREMENT PORTFOLIO ALLOCATION
fig_allocation = px.treemap(retirement_allocation, path=["Asset Class"],
                 values="Percentage",title="Retirement Asset Allocation")
fig_allocation.data[0].textinfo = "label+text+percent root"

fig_allocation.update_layout(margin=dict(l=10,r=0,t=25,b=0))
# RETIREMENT PORTFOLIO ALLOCATION

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_budget, use_container_width=True)
right_column.plotly_chart(fig_allocation, use_container_width=True)

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