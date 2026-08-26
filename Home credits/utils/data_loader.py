from pathlib import Path
import pandas as pd
import streamlit as st

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "application_train.csv"
)

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)

    # Clean column names
    df.columns = [column.strip().upper() for column in df.columns]

    return df