
import pandas as pd
from ydata_profiling import ProfileReport


def suggest_rules(df: pd.DataFrame):
    profile = ProfileReport(df, minimal=True, explorative=True, correlations={"pearson": False})
    suggestions = {"rules": []}

    for col in df.columns:
        col_info = df[col]
        col_rules = []

        if col_info.isnull().any():
            col_rules.append("not_null")

        if col_info.is_unique:
            col_rules.append("unique")

        if pd.api.types.is_numeric_dtype(col_info):
            col_rules.append({
                "range": {
                    "min": float(col_info.min()),
                    "max": float(col_info.max())
                }
            })

        if pd.api.types.is_string_dtype(col_info) and col_info.str.match(r'^\w+$').mean() > 0.8:
            col_rules.append({"pattern": r"^\w+$"})

        if col_rules:
            suggestions["rules"].append({
                "column": col,
                "rules": col_rules
            })

    return suggestions
