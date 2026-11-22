import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Regional Sales Pulse",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 Regional Sales Pulse")
st.subheader("Sales Analysis and Business Performance Dashboard")

st.markdown("---")

# Load dataset
df = pd.read_csv("Sample - Superstore.csv", encoding="cp1252")

# Convert Order Date
df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce"
)

df = df.dropna(subset=["Order Date"])

# Create Year-Month column
df["Year-Month"] = (
    df["Order Date"].dt.to_period("M").astype(str)
)

# Sidebar filter
st.sidebar.header("Dashboard Filters")

regions = sorted(df["Region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

# Filter data
filtered_df = df[
    df["Region"].isin(selected_regions)
]

if filtered_df.empty:
    st.warning("Please select at least one region.")
    st.stop()

# Calculate KPIs
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

# KPI cards
st.header("📌 Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

col4.metric(
    "Total Orders",
    f"{total_orders:,}"
)

st.markdown("---")

# Monthly Sales Trend
st.header("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby("Year-Month")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="Year-Month",
    y="Sales",
    title="Monthly Sales Performance",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# Sales by Region and Category
st.header("🌎 Sales Analysis")

col1, col2 = st.columns(2)

# Sales by Region
with col1:

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Sales by Region",
        text_auto=".2s"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Sales by Category
with col2:

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Sales by Category",
        hole=0.4
    )

    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Profit by Sub-Category
st.header("💰 Profit by Sub-Category")

subcategory_profit = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .reset_index()
    .sort_values("Profit", ascending=True)
)

fig4 = px.bar(
    subcategory_profit,
    x="Profit",
    y="Sub-Category",
    orientation="h",
    title="Profit Analysis by Sub-Category",
    color="Profit"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Discount vs Profit
st.header("📉 Discount vs Profit Analysis")

fig5 = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    hover_data=["Sub-Category", "Sales"],
    title="Relationship Between Discount and Profit"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# Download report
st.header("📥 Download Sales Report")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Report",
    data=csv_data,
    file_name="Regional_Sales_Report.csv",
    mime="text/csv"
)

# Show data
with st.expander("View Sales Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# Footer
st.markdown("---")

st.caption("Regional Sales Pulse | Sales Data Analysis Project")