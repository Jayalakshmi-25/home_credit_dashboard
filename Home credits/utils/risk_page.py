from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from utils.auth import require_login, logout
from utils.charts import (
    bar_chart,
    funnel_chart,
    histogram,
    horizontal_bar_chart,
    line_chart,
    pie_chart,
    polar_chart,
    risk_profile_chart,
    scatter_chart,
    sunburst_chart,
    treemap_chart,
)
from utils.features import group_default
from utils.filters import sidebar_filters, readable_label
from utils.kpis import overview_kpis
from utils.page_helpers import get_prepared_data
from utils.theme import apply_sky_theme, render_page_header, PAGE_SYMBOLS


PAGE_FOCUS = {
    "Executive Overview": ("AGE_YEARS", "Applicant age profile"),
    "Sales Analysis": ("AMT_INCOME_TOTAL", "Income profile"),
    "Profit Analysis": ("AMT_CREDIT", "Credit profile"),
    "Regional Analysis": ("REGION_POPULATION_RELATIVE", "Population density"),
    "State Analysis": ("EXT_SOURCE_2", "External score 2"),
    "City Analysis": ("CNT_FAM_MEMBERS", "Family size"),
    "Category Analysis": ("AMT_INCOME_TOTAL", "Income by occupation"),
    "SubCategory Analysis": ("AMT_INCOME_TOTAL", "Income type distribution"),
    "Product Analysis": ("AMT_CREDIT", "Credit by housing type"),
    "Customer Analysis": ("CNT_CHILDREN", "Children count"),
    "Segment Analysis": ("AMT_CREDIT", "Credit by gender"),
    "Order Analysis": ("AMT_CREDIT", "Loan amount profile"),
    "Shipping Analysis": ("EMPLOYMENT_YEARS", "Employment duration"),
    "Discount Analysis": ("CREDIT_TO_INCOME", "Credit-to-income ratio"),
    "Loss Analysis": ("EXT_SOURCE_3", "External score 3"),
    "Time Series": ("AGE_YEARS", "Age risk curve"),
    "Growth Analysis": ("EMPLOYMENT_YEARS", "Employment duration curve"),
    "Sales vs Profit": ("AMT_GOODS_PRICE", "Goods price profile"),
    "Top Bottom": ("EXT_SOURCE_1", "External score 1"),
    "Data Explorer": ("HOUR_APPR_PROCESS_START", "Application hour"),
}

PAGE_CHARTS = {
    "Executive Overview": "donut", "Sales Analysis": "horizontal",
    "Profit Analysis": "treemap", "Regional Analysis": "polar",
    "State Analysis": "funnel", "City Analysis": "histogram",
    "Category Analysis": "sunburst", "SubCategory Analysis": "donut",
    "Product Analysis": "scatter", "Customer Analysis": "horizontal",
    "Segment Analysis": "polar", "Order Analysis": "histogram",
    "Shipping Analysis": "funnel", "Discount Analysis": "treemap",
    "Loss Analysis": "donut", "Time Series": "line",
    "Growth Analysis": "scatter", "Sales vs Profit": "sunburst",
    "Top Bottom": "horizontal", "Data Explorer": "polar",
}


def _primary_chart(grouped, group_column, title):
    chart_type = PAGE_CHARTS.get(title, "bar")
    chart_title = f"{title}: default risk profile"
    if chart_type == "donut":
        return pie_chart(grouped, group_column, "count", chart_title, hole=0.58)
    if chart_type == "horizontal":
        return horizontal_bar_chart(grouped.sort_values("default_rate"), "default_rate", group_column, chart_title)
    if chart_type == "treemap":
        return treemap_chart(grouped, [group_column], "count", chart_title)
    if chart_type == "sunburst":
        return sunburst_chart(grouped, [group_column], "count", chart_title)
    if chart_type == "funnel":
        return funnel_chart(grouped, "count", group_column, chart_title)
    if chart_type == "polar":
        return polar_chart(grouped, group_column, "default_rate", chart_title)
    if chart_type == "histogram":
        return histogram(grouped, "default_rate", title=chart_title, nbins=10)
    if chart_type == "line":
        return line_chart(grouped, group_column, "default_rate", chart_title)
    if chart_type == "scatter":
        return scatter_chart(grouped, "count", "default_rate", group_column, chart_title)
    return bar_chart(grouped, group_column, "default_rate", chart_title)


def render_risk_page(title, group_column):
    st.set_page_config(page_title=title, layout="wide")
    require_login()
    apply_sky_theme()
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()
    render_page_header(
        title,
        subtitle="Borrower Risk Intelligence",
        kicker="HOME CREDIT / BORROWER RISK INTELLIGENCE",
    )
    st.title(f"{PAGE_SYMBOLS.get(title, '🏠')} {title}")
    st.caption("Filtered borrower behavior, default exposure, and portfolio signals")
    st.markdown(f'<div class="chart-badge">PRIMARY VIEW · {PAGE_CHARTS.get(title, "bar").upper()} CHART</div>', unsafe_allow_html=True)

    df = get_prepared_data()
    if df.empty:
        st.error("No data was found at data/application_train.csv.")
        st.stop()

    filtered_df = sidebar_filters(df)
    if filtered_df.empty:
        st.warning("No applications match the selected filters.")
        st.stop()

    metrics = overview_kpis(filtered_df)
    columns = st.columns(4)
    columns[0].metric("📋 Applications", f"{metrics['applications']:,}")
    columns[1].metric("⚠️ Default Rate", f"{metrics['default_rate']:.2f}%")
    columns[2].metric("📊 Average Income", f"{metrics['avg_income']:,.0f}")
    columns[3].metric("💳 Average Credit", f"{metrics['avg_credit']:,.0f}")

    if group_column not in filtered_df.columns:
        st.info(f"The dataset does not contain {group_column}.")
        return

    grouped = group_default(filtered_df, group_column)
    if grouped.empty:
        st.info("No risk breakdown is available for the selected filters.")
        return

    group_label = readable_label(group_column)
    st.subheader(f"Default risk by {group_label}")
    chart_columns = st.columns(3)
    with chart_columns[0]:
        st.plotly_chart(risk_profile_chart(grouped, group_column, f"{title}: default risk profile"), use_container_width=True, height=360)
    with chart_columns[1]:
        st.plotly_chart(bar_chart(grouped, group_column, "count", "Applications by group"), use_container_width=True, height=360)
    with chart_columns[2]:
        st.plotly_chart(scatter_chart(grouped, "count", "default_rate", group_column, "Risk versus applicant volume"), use_container_width=True, height=360)

    numeric_column, numeric_label = PAGE_FOCUS.get(title, ("AMT_INCOME_TOTAL", "Income distribution"))
    if numeric_column in filtered_df.columns:
        focus_columns = st.columns(2)
        with focus_columns[0]:
            st.plotly_chart(histogram(filtered_df, numeric_column, title=numeric_label, nbins=40, log_x=numeric_column in {"AMT_INCOME_TOTAL", "AMT_CREDIT"}), use_container_width=True, height=360)
        with focus_columns[1]:
            if numeric_column == "AMT_CREDIT":
                relationship = filtered_df[[numeric_column, "TARGET"]].dropna().rename(columns={"TARGET": "default_flag"})
                if len(relationship) > 5000:
                    relationship = relationship.sample(5000, random_state=42)
                st.plotly_chart(scatter_chart(relationship, numeric_column, "default_flag", None, f"{numeric_label} versus default outcome"), use_container_width=True, height=360)
            else:
                relationship = filtered_df[[numeric_column, "AMT_CREDIT", "TARGET"]].dropna()
                if len(relationship) > 5000:
                    relationship = relationship.sample(5000, random_state=42)
                st.plotly_chart(scatter_chart(relationship, numeric_column, "AMT_CREDIT", "TARGET", f"{numeric_label} versus credit"), use_container_width=True, height=360)

    with st.expander("Filtered application data"):
        st.dataframe(filtered_df.head(100), width="stretch", hide_index=True)
        st.download_button("Download filtered page data", filtered_df.to_csv(index=False), f"{title.lower().replace(' ', '_')}.csv", "text/csv", width="stretch")
