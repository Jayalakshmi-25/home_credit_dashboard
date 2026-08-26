import pandas as pd
import streamlit as st

COLUMN_LABELS = {
    "SK_ID_CURR": "Applicant ID",
    "NAME_CONTRACT_TYPE": "Contract Type",
    "CODE_GENDER": "Gender",
    "NAME_EDUCATION_TYPE": "Education",
    "TARGET": "Target",
    "AMT_INCOME_TOTAL": "Income",
    "AMT_CREDIT": "Credit",
    "AGE_YEARS": "Age",
    "NAME_INCOME_TYPE": "Income Type",
    "NAME_HOUSING_TYPE": "Housing Type",
    "NAME_FAMILY_STATUS": "Family Status",
    "REGION_RATING_CLIENT": "Region Rating",
    "REG_REGION_NOT_LIVE_REGION": "State Region",
    "REG_CITY_NOT_LIVE_CITY": "City Status",
    "OCCUPATION_TYPE": "Occupation",
    "FLAG_OWN_CAR": "Own Car",
    "WEEKDAY_APPR_PROCESS_START": "Application Weekday",
    "EMPLOYMENT_YEARS": "Employment Years",
    "EXT_SOURCE_2": "External Score 2",
    "EXT_SOURCE_3": "External Score 3",
    "CREDIT_TO_INCOME": "Credit-to-Income Ratio",
    "HOUR_APPR_PROCESS_START": "Application Hour",
    "AMT_GOODS_PRICE": "Goods Price",
    "ORGANIZATION_TYPE": "Organization Type",
    "CNT_FAM_MEMBERS": "Family Members",
    "CNT_CHILDREN": "Children Count",
    "REGION_POPULATION_RELATIVE": "Population Relative",
}


def readable_label(column_name):
    return COLUMN_LABELS.get(column_name, column_name.replace("_", " ").title())


def sidebar_filters(df):

    filtered = df.copy()
    st.sidebar.header("Dashboard Filters")

    if "SK_ID_CURR" in filtered.columns:
        applicant_search = st.sidebar.text_input(
            readable_label("SK_ID_CURR"),
            placeholder="Enter an applicant ID",
        ).strip()

        if applicant_search:
            filtered = filtered[
                filtered["SK_ID_CURR"].astype(str).str.contains(
                    applicant_search,
                    case=False,
                    na=False,
                )
            ]

    # Contract type
    if "NAME_CONTRACT_TYPE" in filtered.columns:

        options = sorted(
            filtered["NAME_CONTRACT_TYPE"]
            .dropna()
            .unique()
        )

        selected = st.sidebar.multiselect(
            readable_label("NAME_CONTRACT_TYPE"),
            options,
            default=options
        )

        filtered = filtered[
            filtered["NAME_CONTRACT_TYPE"].isin(selected)
        ]

    # Gender
    if "CODE_GENDER" in filtered.columns:

        options = sorted(
            filtered["CODE_GENDER"]
            .dropna()
            .unique()
        )

        selected = st.sidebar.multiselect(
            readable_label("CODE_GENDER"),
            options,
            default=options
        )

        filtered = filtered[
            filtered["CODE_GENDER"].isin(selected)
        ]

    # Education
    if "NAME_EDUCATION_TYPE" in filtered.columns:

        options = sorted(
            filtered["NAME_EDUCATION_TYPE"]
            .dropna()
            .unique()
        )

        selected = st.sidebar.multiselect(
            readable_label("NAME_EDUCATION_TYPE"),
            options,
            default=options
        )

        filtered = filtered[
            filtered["NAME_EDUCATION_TYPE"].isin(selected)
        ]

    # Default
    if "TARGET" in filtered.columns:

        selected_target = st.sidebar.multiselect(
            readable_label("TARGET"),
            [0, 1],
            default=[0, 1],
            format_func=lambda value:
                "Default / Difficulty"
                if value == 1
                else "No Default"
        )

        filtered = filtered[
            filtered["TARGET"].isin(selected_target)
        ]

    numeric_filters = [
        ("AMT_INCOME_TOTAL", "Income range"),
        ("AMT_CREDIT", "Credit range"),
        ("AGE_YEARS", "Age range"),
    ]
    for column, label in numeric_filters:
        if column not in filtered.columns or filtered.empty:
            continue

        numeric_values = pd.to_numeric(
            filtered[column],
            errors="coerce",
        ).replace([float("inf"), float("-inf")], pd.NA).dropna()
        if numeric_values.empty:
            continue

        minimum = float(numeric_values.min())
        maximum = float(numeric_values.max())
        if minimum >= maximum:
            continue

        selected_range = st.sidebar.slider(
            label,
            min_value=minimum,
            max_value=maximum,
            value=(minimum, maximum),
        )
        filtered = filtered[
            filtered[column].between(selected_range[0], selected_range[1])
        ]

    return filtered


def apply_filters(df, filters):
    """Return the filtered frame produced by sidebar_filters.

    Kept for compatibility with pages that use the older two-step API.
    """
    if filters is None:
        return df.copy()

    return filters.copy()