import pandas as pd


def available(df, columns):

    return all(
        column in df.columns
        for column in columns
    )


def default_rate(df):

    if "TARGET" not in df.columns:
        return 0.0

    if len(df) == 0:
        return 0.0

    return df["TARGET"].mean() * 100


def group_default(df, group_column):

    if not available(
        df,
        [group_column, "TARGET"]
    ):
        return pd.DataFrame()

    data = df[[group_column, "TARGET"]].copy()
    group_key = "__group_key__"
    target_key = "__target_value__"

    data = data.rename(columns={group_column: group_key, "TARGET": target_key})

    if pd.api.types.is_numeric_dtype(data[group_key]):
        data[group_key] = pd.qcut(
            data[group_key],
            q=10,
            duplicates="drop",
        ).astype("string")

    result = (
        data.groupby(
            group_key,
            dropna=False,
            observed=False,
        )[target_key]
        .agg(["count", "mean"])
        .reset_index()
        .rename(columns={group_key: group_column, "mean": "default_rate"})
    )

    result["default_rate"] = result["default_rate"] * 100

    if len(result) == 0:
        return result

    risk_scores = result["default_rate"].rank(method="first", pct=True)

    if len(result) == 1:
        result["risk_level"] = ["Medium risk"]
        return result

    if len(result) == 2:
        result["risk_level"] = [
            "Low risk" if score <= 0.5 else "High risk"
            for score in risk_scores
        ]
        return result

    result["risk_level"] = pd.cut(
        risk_scores,
        bins=[0, 0.33, 0.66, 1.0],
        labels=["Low risk", "Medium risk", "High risk"],
        include_lowest=True,
        right=True,
    )

    return result