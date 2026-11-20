import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IT Support Tickets Dashboard", layout="wide")
st.title("🎫 IT Support Tickets Analytics Dashboard")
st.markdown("Interactive KPI & Ticket Analysis powered by **Python & Streamlit** (Companion to Power BI & SQL Analysis).")

# Load cleaned Excel dataset
@st.cache_data
def load_data():
    return pd.read_excel("IT_Support_Tickets_Cleaned.xlsx")

df = load_data()

# Sidebar dynamic filters for categorical columns
st.sidebar.header("Filter Tickets")
filtered_df = df.copy()

cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
for col in cat_cols:
    unique_vals = df[col].dropna().unique().tolist()
    if 1 < len(unique_vals) <= 20:
        selected = st.sidebar.multiselect(f"{col}", unique_vals, default=unique_vals)
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

# Top KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Filtered Tickets", f"{len(filtered_df):,}")
col2.metric("Total Columns Tracked", len(filtered_df.columns))
col3.metric("Dataset Completeness", f"{(1 - filtered_df.isna().mean().mean())*100:.1f}%")

st.divider()

# Interactive Charts
chart_cols = [c for c in cat_cols if 1 < df[c].nunique() <= 15]
if len(chart_cols) >= 2:
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.bar(filtered_df[chart_cols].value_counts().reset_index(),
                      x=chart_cols, y="count", title=f"Tickets by {chart_cols}", color=chart_cols)
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.pie(filtered_df, names=chart_cols, title=f"Distribution by {chart_cols}", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)
elif len(chart_cols) == 1:
    fig1 = px.bar(filtered_df[chart_cols].value_counts().reset_index(),
                  x=chart_cols, y="count", title=f"Tickets by {chart_cols}")
    st.plotly_chart(fig1, use_container_width=True)

# Data Table & Power BI Preview Tab
tab1, tab2 = st.tabs(["📊 Interactive Ticket Data", "🖼️ Power BI Report Preview"])
with tab1:
    st.dataframe(filtered_df, use_container_width=True)
with tab2:
    st.image("dashboard_preview.png", caption="Original Power BI Desktop Dashboard", use_container_width=True)
