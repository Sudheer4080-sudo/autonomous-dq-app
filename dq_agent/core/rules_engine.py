
import pandas as pd

def apply_rules(df: pd.DataFrame, config: dict) -> list:
    """
    Applies validation rules to a DataFrame based on config.
    Returns list of row indices that failed.
    """
    failed_indices = set()

    for rule in config.get("rules", []):
        col = rule["column"]
        for r in rule["rules"]:
            if r == "not_null":
                failed = df[df[col].isnull()].index
            elif r == "unique":
                failed = df[df[col].duplicated()].index
            elif isinstance(r, dict) and "range" in r:
                min_val = r["range"].get("min", float("-inf"))
                max_val = r["range"].get("max", float("inf"))
                failed = df[(df[col] < min_val) | (df[col] > max_val)].index
            elif isinstance(r, dict) and "pattern" in r:
                pattern = r["pattern"]
                failed = df[~df[col].astype(str).str.match(pattern)].index
            else:
                failed = []

            failed_indices.update(failed)

    return list(failed_indices)
