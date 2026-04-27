"""
views.py - Dashboard Page Layouts.
Orchestrates metrics, charts, and funnel logic into structured Streamlit views.
"""
import streamlit as st
from db import db_engine
from metrics import SalesMetrics
from charts import ChartFactory
from funnel import SalesFunnel

class DashboardViews:
    @staticmethod
    def show_overview():
        st.subheader("🚀 Sales Overview")
        df = db_engine.get_revenue_by_dimension("region")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Revenue", f"${df['total_revenue'].sum():,.0f}")
        c2.metric("Active Regions", len(df))
        c3.metric("Goal Attainment", "84%")
        
        c_left, c_right = st.columns(2)
        with c_left:
            st.plotly_chart(ChartFactory.bar_revenue(df, "region", "Revenue by Region"), use_container_width=True)
        with c_right:
            stage_df = db_engine.get_stage_counts()
            st.plotly_chart(ChartFactory.bar_revenue(stage_df.rename({"deal_count": "total_revenue"}), "stage", "Deals by Stage"), use_container_width=True)

    @staticmethod
    def show_regional_breakdown():
        st.subheader("📍 Regional Performance")
        raw = db_engine.get_date_range_slice("2000-01-01", "2099-12-31")
        st.plotly_chart(ChartFactory.heatmap_rep_region(raw), use_container_width=True)

    @staticmethod
    def show_funnel_analysis():
        st.subheader("🌪️ Pipeline Conversion")
        raw = db_engine.get_date_range_slice("2000-01-01", "2099-12-31")
        f_df = SalesFunnel.process_funnel_data(raw)
        st.plotly_chart(SalesFunnel.create_funnel_chart(f_df), use_container_width=True)
        st.dataframe(f_df, use_container_width=True)

    @staticmethod
    def show_rep_performance():
        st.subheader("👤 Rep Leaderboard")
        rep_df = db_engine.get_revenue_by_dimension("rep")
        
        # THE FIX IS HERE: Added "rep" as the second argument
        rankings = SalesMetrics.get_rankings(rep_df, "rep")
        
        st.markdown("### Top Performers")
        st.table(rankings["top"].to_pandas())
