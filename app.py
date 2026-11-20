import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IT Support Ticket & Resolution Performance Analysis", layout="wide")
st.title("🎫 IT Support Ticket & Resolution Performance Analysis")
st.markdown("Interactive KPI & Resolution Dashboard (Companion to Power BI & SQL Analysis)")

@st.cache_data
def load_data():
    df = pd.read_excel("IT_Support_Tickets_Cleaned.xlsx")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

df = load_data()

# Sidebar Filters matching your Power BI slicers (priority, status, sla_plan)
st.sidebar.header("Dashboard Slicers")
filtered_df = df.copy()

for col in ["priority", "status", "sla_plan"]:
    if col in filtered_df.columns:
        options = filtered_df[col].dropna().unique().tolist()
        selected = st.sidebar.multiselect(col.replace("_", " ").title(), options, default=options)
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

# Top 4 KPI Cards matching your Power BI report
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tickets", f"{len(filtered_df):,}")

res_col = next((c for c in filtered_df.columns if "resolution" in c and "hour" in c), None)
c2.metric("Avg Resolution Hours", f"{filtered_df[res_col].mean():.2f}" if res_col else "N/A")

active_count = len(filtered_df[filtered_df["status"].astype(str).str.lower().isin(["open", "in progress", "active", "pending"])]) if "status" in filtered_df.columns else 0
c3.metric("Active Tickets", f"{active_count:,}")

csat_col = next((c for c in filtered_df.columns if "csat" in c), None)
c4.metric("Avg CSAT Score", f"{filtered_df[csat_col].mean():.2f}" if csat_col else "N/A")

st.divider()

# Row 1 Charts: Total Tickets by Year & Total Tickets by issue_type
col_left, col_right = st.columns(2)

with col_left:
    date_col = next((c for c in filtered_df.columns if "date" in c or "year" in c or "created" in c), None)
    if date_col:
        temp_df = filtered_df.copy()
        if "year" not in date_col:
            temp_df["year"] = pd.to_datetime(temp_df[date_col], errors="coerce").dt.year
        else:
            temp_df["year"] = temp_df[date_col]
        year_counts = temp_df.groupby("year").size().reset_index(name="Total Tickets").dropna()
        fig_year = px.line(year_counts, x="year", y="Total Tickets", markers=True, title="Total Tickets by Year")
        st.plotly_chart(fig_year, use_container_width=True)

with col_right:
    if "issue_type" in filtered_df.columns:
        issue_counts = filtered_df["issue_type"].value_counts().reset_index()
        issue_counts.columns = ["issue_type", "Total Tickets"]
        fig_issue = px.bar(issue_counts, x="Total Tickets", y="issue_type", orientation="h",
                           title="Total Tickets by Issue Type", text="Total Tickets")
        fig_issue.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_issue, use_container_width=True)

# Row 2 Charts: Avg Resolution Hours by sla_plan & priority + Total Tickets by priority
col_b1, col_b2 = st.columns(2)

with col_b1:
    if res_col and "sla_plan" in filtered_df.columns and "priority" in filtered_df.columns:
        sla_df = filtered_df.groupby(["sla_plan", "priority"])[res_col].mean().reset_index()
        fig_sla = px.bar(sla_df, x="sla_plan", y=res_col, color="priority", barmode="group",
                         title="Avg Resolution Hours by SLA Plan and Priority")
        st.plotly_chart(fig_sla, use_container_width=True)

with col_b2:
    if "priority" in filtered_df.columns:
        fig_prio = px.pie(filtered_df, names="priority", title="Total Tickets by Priority", hole=0.5)
        st.plotly_chart(fig_prio, use_container_width=True)

# Tabs for Raw Data and Power BI Screenshot
tab1, tab2 = st.tabs(["📊 Ticket Records", "🖼️ Original Power BI Report"])
with tab1:
    st.dataframe(filtered_df, use_container_width=True)
with tab2:
    st.image("dashboard_preview.png", caption="Power BI Desktop Report", use_container_width=True)
