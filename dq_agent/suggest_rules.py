
import pandas as pd
from pandas_profiling import ProfileReport

def suggest_rules(df):
    profile = ProfileReport(df, minimal=True)
    rules = []
    for col in df.columns:
        col_rules = {"column": col, "rules": []}
        if df[col].isnull().sum() == 0:
            col_rules["rules"].append("not_null")
        if df[col].is_unique:
            col_rules["rules"].append("unique")
        if pd.api.types.is_numeric_dtype(df[col]):
            col_rules["rules"].append({
                "range": {
                    "min": float(df[col].min()),
                    "max": float(df[col].max())
                }
            })
        rules.append(col_rules)
    return {"rules": rules}
