import streamlit as st
import pandas as pd
import plotly.express as px

df=pd.read_csv("Sample - Superstore.csv",encoding="cp1252")
print(df.head())
print(df.info())
df["Order Date"]=pd.to_datetime(df["Order Date"])
df["Year-Month"]=df["Order Date"].dt.to_period("M").astype(str)
regions=sorted(df["Region"].unique())
selected_regions=st.sidebar.multiselect("Select Region",regions,default=regions)
df=df[df["Region"].isin(selected_regions)]
total_sales=df["Sales"].sum()
total_profit=df["Profit"].sum()
total_orders=df["Order ID"].nunique()
profit_margin=(total_profit/total_sales)*100

col1,col2,col3,col4=st.columns(4)
col1=st.metric("Total Sales",f"${total_sales:,.2f}")
col1=st.metric("Total Profit",f"${total_profit:,.2f}")
col1=st.metric("Profit Margin",f"{profit_margin:.2f}%")
col1=st.metric("Number of Orders",f"{total_orders:,}")

monthly_sales=df.groupby("Year-Month")["Sales"].sum()
fig=px.line(monthly_sales,title="Monthly Sales Trend")
st.plotly_chart(fig)
subcategory_profit=(df.groupby("Sub-Category")["Profit"].sum())
fig=px.bar(subcategory_profit,title="Profit by Sub-Category")
st.plotly_chart(fig)
discount_profit=(df.groupby("Discount")["Profit"].mean())
fig=px.line(discount_profit,title="Discount vs Profit")
st.plotly_chart(fig)
