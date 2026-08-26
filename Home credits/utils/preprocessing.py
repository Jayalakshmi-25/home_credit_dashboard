import numpy as np
import pandas as pd


def clean_data(df):
    data = df.copy()

    numeric_columns = data.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:
        data[column] = data[column].replace(
            [np.inf, -np.inf],
            np.nan
        )

    return data


def add_features(df):
    data = df.copy()

    # Income per family member
    if {
        "AMT_INCOME_TOTAL",
        "CNT_FAM_MEMBERS"
    }.issubset(data.columns):

        data["INCOME_PER_FAMILY_MEMBER"] = (
            data["AMT_INCOME_TOTAL"]
            / data["CNT_FAM_MEMBERS"].replace(0, np.nan)
        )

    # Credit-to-income ratio
    if {
        "AMT_CREDIT",
        "AMT_INCOME_TOTAL"
    }.issubset(data.columns):

        data["CREDIT_TO_INCOME"] = (
            data["AMT_CREDIT"]
            / data["AMT_INCOME_TOTAL"].replace(0, np.nan)
        )

    # Annuity-to-income ratio
    if {
        "AMT_ANNUITY",
        "AMT_INCOME_TOTAL"
    }.issubset(data.columns):

        data["ANNUITY_TO_INCOME"] = (
            data["AMT_ANNUITY"]
            / data["AMT_INCOME_TOTAL"].replace(0, np.nan)
        )

    # Annuity-to-credit ratio
    if {
        "AMT_ANNUITY",
        "AMT_CREDIT"
    }.issubset(data.columns):

        data["ANNUITY_TO_CREDIT"] = (
            data["AMT_ANNUITY"]
            / data["AMT_CREDIT"].replace(0, np.nan)
        )

    # Age
    if "DAYS_BIRTH" in data.columns:

        data["AGE_YEARS"] = (
            -data["DAYS_BIRTH"] / 365.25
        ).round(1)

    # Employment duration
    if "DAYS_EMPLOYED" in data.columns:

        employed = data["DAYS_EMPLOYED"].copy()

        # Positive values in this column can represent
        # unusual/unknown employment values.
        employed = employed.where(
            employed < 0,
            np.nan
        )

        data["EMPLOYMENT_YEARS"] = (
            -employed / 365.25
        ).round(1)

    # Years since phone change
    if "DAYS_LAST_PHONE_CHANGE" in data.columns:

        data["PHONE_CHANGE_YEARS"] = (
            -data["DAYS_LAST_PHONE_CHANGE"] / 365.25
        ).round(1)

    return data


def prepare_data(df):
    data = clean_data(df)

    data = add_features(data)

    return data