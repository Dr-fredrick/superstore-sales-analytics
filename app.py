import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# Dashboard UI layout configuration
st.set_page_config(page_title="SuperStore Sales Analytics", layout="wide")

DB_PATH = os.path.join("data", "processed", "superstore.db")

@st.cache_data
def run_query(query):
    """Helper function to isolate connection logic and return dataframes"""
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)

# --------------------------------------------------------------------
# SQL QUERIES FOR METRICS & CHARTS
# --------------------------------------------------------------------

# Main KPI aggregation query
kpi_query = """
SELECT 
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales;
"""

# Profit analysis by sub-category for horizontal bar chart
product_query = """
SELECT sub_category, ROUND(SUM(sales), 2) AS total_sales, ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY sub_category
ORDER BY total_profit DESC
LIMIT 10;
"""

# Geographical sales aggregation for donut/pie chart
geo_query = """
SELECT state, ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY state
ORDER BY total_sales DESC
LIMIT 10;
"""

# Data Ingestion from SQLite
df_kpi = run_query(kpi_query)
df_product = run_query(product_query)
df_geo = run_query(geo_query)

# --------------------------------------------------------------------
# STREAMLIT FRONTEND RENDERING
# --------------------------------------------------------------------
st.title("📊 SuperStore Executive Sales Dashboard")
st.markdown("Automated enterprise-level insights driven by Python, SQL, and Streamlit.")
st.markdown("---")

# Row 1: KPI Metrics Display
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"${df_kpi['total_revenue'][0]:,.2f}")
with col2:
    st.metric("Total Profit", f"${df_kpi['total_profit'][0]:,.2f}")
with col3:
    st.metric("Profit Margin", f"{df_kpi['profit_margin'][0]}%")
with col4:
    st.metric("Total Orders", f"{df_kpi['total_orders'][0]:,}")

st.markdown("---")

# Row 2: Visualizations Layout
left_chart_col, right_chart_col = st.columns(2)

with left_chart_col:
    st.subheader("📦 Top 10 Sub-Categories by Profit")
    fig_prod = px.bar(
        df_product, 
        x="total_profit", 
        y="sub_category", 
        orientation='h',
        color="total_profit",
        color_continuous_scale="Viridis",
        labels={"total_profit": "Net Profit ($)", "sub_category": "Sub-Category"}
    )
    # Ensure ascending category sorting for horizontal bar presentation
    fig_prod.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig_prod, use_container_width=True)

with right_chart_col:
    st.subheader("🌎 Top 10 States by Sales Volume")
    fig_geo = px.pie(
        df_geo, 
        values="total_sales", 
        names="state", 
        hole=0.4, # Donut chart formatting
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_geo, use_container_width=True)