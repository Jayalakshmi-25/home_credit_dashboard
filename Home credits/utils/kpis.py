def overview_kpis(df):

    return {
        "applications": len(df),

        "default_rate":
            df["TARGET"].mean() * 100
            if "TARGET" in df.columns
            else 0,

        "avg_income":
            df["AMT_INCOME_TOTAL"].mean()
            if "AMT_INCOME_TOTAL" in df.columns
            else 0,

        "avg_credit":
            df["AMT_CREDIT"].mean()
            if "AMT_CREDIT" in df.columns
            else 0,
    }