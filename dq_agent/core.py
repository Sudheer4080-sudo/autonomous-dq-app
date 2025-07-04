
import pandas as pd

def apply_rules(df, config):
    results = []
    for rule in config.get("rules", []):
        col = rule["column"]
        for check in rule["rules"]:
            if check == "not_null":
                failed = df[df[col].isnull()]
                if not failed.empty:
                    results.append({"rule": f"{col} must not be null", "rows": failed})
            elif check == "unique":
                failed = df[df.duplicated(col)]
                if not failed.empty:
                    results.append({"rule": f"{col} must be unique", "rows": failed})
            elif isinstance(check, dict) and "range" in check:
                min_val, max_val = check["range"]["min"], check["range"]["max"]
                failed = df[(df[col] < min_val) | (df[col] > max_val)]
                if not failed.empty:
                    results.append({"rule": f"{col} out of range", "rows": failed})
            elif isinstance(check, dict) and "pattern" in check:
                failed = df[~df[col].astype(str).str.match(check["pattern"])]
                if not failed.empty:
                    results.append({"rule": f"{col} regex mismatch", "rows": failed})
    return results
