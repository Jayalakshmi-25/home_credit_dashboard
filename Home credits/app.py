import streamlit as st

from utils.auth import logout, require_login
from utils.filters import sidebar_filters
from utils.charts import bar_chart, scatter_chart

from utils.kpis import overview_kpis
from utils.features import group_default
from utils.page_helpers import get_prepared_data

from utils.theme import apply_sky_theme, render_page_header

st.set_page_config(
page_title="💳 Home Credit Dashboard",
page_icon="HC",
layout="wide",
)

require_login()
apply_sky_theme()

render_page_header(
    "Home Credit Risk Overview",
    symbol="🏠",
    subtitle="Risk Intelligence",
    kicker="HOME CREDIT DASHBOARD",
)
st.title("🏠 Home Credit Risk Overview")
st.caption("Credit Risk Analysis · exposure and default signals")
st.markdown(
    '<div class="chart-badge">PRIMARY VIEW · FILTERED PORTFOLIO</div>',
    unsafe_allow_html=True,
)


if st.sidebar.button("Logout"):
    logout()
    st.rerun()

if st.button(" 🔄 Reload Data"):
    st.rerun()


df = get_prepared_data()

if df.empty:

    st.error("No data was found at data/application_train.csv.")
    st.stop()


filtered_df = sidebar_filters(df)


search_fields = {

    "No additional search": None,

    "Applicant ID": "SK_ID_CURR",

    "Contract Type": "NAME_CONTRACT_TYPE",

    "Gender": "CODE_GENDER",

    "Education": "NAME_EDUCATION_TYPE",

    "Income Type": "NAME_INCOME_TYPE",

    "Housing Type": "NAME_HOUSING_TYPE",

    "Family Status": "NAME_FAMILY_STATUS",

}

def jls_extract_def():
    return " Dashboard search"


with st.expander(jls_extract_def()):
    search_label = st.selectbox(
        "Choose a field to search",
        list(search_fields),
    )
    search_value = st.text_input(
        "Search value",
        placeholder="Type a value to filter the selected field",
        disabled=search_fields[search_label] is None,
    )

search_column = search_fields[search_label]
if search_column and search_value.strip():
    filtered_df = filtered_df[
        filtered_df[search_column].astype(str).str.contains(
            search_value.strip(),

            case=False,

            na=False,
        )

    ]


if filtered_df.empty:

    st.warning("No applications match the selected filters.")
    st.stop()


metrics = overview_kpis(filtered_df)

columns = st.columns(4)

columns[0].metric("📋 Applications", f"{metrics['applications']:,}")

columns[1].metric("⚠️ Default Rate", f"{metrics['default_rate']:.2f}%")

columns[2].metric("📊 Average Income", f"{metrics['avg_income']:,.0f}")

columns[3].metric("💳 Average Credit", f"{metrics['avg_credit']:,.0f}")

st.caption(f"Showing {len(filtered_df):,} applications after applying filters.")

st.subheader("Filtered Risk Signals")
chart_columns = st.columns(2)

with chart_columns[0]:
    education_risk = group_default(filtered_df, "NAME_EDUCATION_TYPE")
    if not education_risk.empty:
        st.plotly_chart(
            bar_chart(
                education_risk,
                "NAME_EDUCATION_TYPE",
                "default_rate",
                "Default Rate by Education",
            ),
            use_container_width=True,
            height=380,
        )

with chart_columns[1]:
    scatter_columns = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "TARGET"]
    if set(scatter_columns).issubset(filtered_df.columns):
        scatter_data = filtered_df[scatter_columns].dropna()
        if len(scatter_data) > 5000:
            scatter_data = scatter_data.sample(5000, random_state=42)
        st.plotly_chart(
            scatter_chart(
                scatter_data,
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "TARGET",
                "Income versus Credit by Default Outcome",
            ),
            width=True,
            height=380,
        )


st.subheader("Filtered Application Data")

st.dataframe(filtered_df.head(100), width="stretch", hide_index=True)

st.download_button(
    "Download filtered applications",
    data=filtered_df.to_csv(index=False),
    file_name="home_credit_filtered_applications.csv",
    mime="text/csv",
    width="stretch",
)


