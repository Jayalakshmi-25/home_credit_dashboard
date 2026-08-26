import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.data_loader import load_data
from utils.preprocessing import prepare_data


@st.cache_data
def get_prepared_data():

    df = load_data()

    return prepare_data(df)


def load_superstore_data():
    return get_prepared_data()


def page_setup(
    title,
    description=""
):

    st.title(title)

    if description:
        st.caption(description)


def show_missing_column(columns):

    st.warning(
        "Required column(s) not available: "
        + ", ".join(columns)
    )

    st.stop()


def risk_summary(df):

    if "TARGET" not in df.columns:
        return

    default_rate = (
        df["TARGET"].mean() * 100
    )

    st.metric(
        "Default Rate",
        f"{default_rate:.2f}%"
    )