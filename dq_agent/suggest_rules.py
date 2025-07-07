import pandas as pd
import re

def is_email(col):
    return col.dropna().str.contains(r"^[^@]+@[^@]+\.[^@]+$", na=False).mean() > 0.5

def is_id(col):
    return col.dropna().str.match(r"^[A-Za-z0-9_-]{6,}$").mean() > 0.5

def suggest_rules(df):
    suggestions = {"rules": []}

    for col in df.columns:
        col_data = df[col]
        rules = []

        # Not null
        if col_data.isnull().sum() == 0:
            rules.append("not_null")

        # Unique
        if col_data.is_unique:
            rules.append("unique")

        # Numeric: Range rule
        if pd.api.types.is_numeric_dtype(col_data):
            rules.append({
                "range": {
                    "min": float(col_data.min()),
                    "max": float(col_data.max())
                }
            })

        # String columns
        if pd.api.types.is_string_dtype(col_data):
            if is_email(col_data):
                rules.append({"pattern": r"[^@]+@[^@]+\.[^@]+"})
            elif is_id(col_data):
                rules.append({"pattern": r"^[A-Za-z0-9_-]{6,}$"})

        # Datetime
        if pd.api.types.is_datetime64_any_dtype(col_data):
            rules.append({
                "range": {
                    "min": str(col_data.min().date()),
                    "max": str(col_data.max().date())
                }
            })

        suggestions["rules"].append({
            "column": col,
            "rules": rules
        })

    return suggestions

