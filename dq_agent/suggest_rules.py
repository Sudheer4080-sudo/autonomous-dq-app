
import pandas as pd

def suggest_rules(df):
    suggestions = {"rules": []}

    for col in df.columns:
        rules = []

        # Rule: not null
        if df[col].isnull().sum() == 0:
            rules.append("not_null")

        # Rule: unique
        if df[col].is_unique:
            rules.append("unique")

        # Rule: numeric range
        if pd.api.types.is_numeric_dtype(df[col]):
            rules.append({
                "range": {
                    "min": float(df[col].min()),
                    "max": float(df[col].max())
                }
            })

        # Rule: simple pattern for emails or identifiers
        if pd.api.types.is_string_dtype(df[col]):
            if df[col].str.contains("@").mean() > 0.5:
                rules.append({"pattern": r"[^@]+@[^@]+\.[^@]+"})

        suggestions["rules"].append({
            "column": col,
            "rules": rules
        })

    return suggestions
