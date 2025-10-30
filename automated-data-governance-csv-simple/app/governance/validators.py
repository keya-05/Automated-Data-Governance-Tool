
import pandas as pd

TYPE_MAP={"int":"Int64","float":"float64","str":"string","date":"string"}

def coerce_types(df, schema):
    df2 = df.copy()
    for col, spec in schema.items():
        if col not in df2.columns:
            df2[col] = pd.NA
        t = spec.get("type", "str")
        if t == "date":
            fmt = spec.get("format", "%Y-%m-%d")
            df2[col] = pd.to_datetime(df2[col], errors="coerce", format=fmt)
        elif t in ("int", "float"):
            # Safe numeric conversion even with NAs
            df2[col] = pd.to_numeric(df2[col], errors="coerce")
        else:
            df2[col] = df2[col].astype("string", copy=False)
    return df2

def run_required_checks(df,schema):
    miss=[]
    for col,spec in schema.items():
        if spec.get("required",False):
            if col not in df or df[col].isna().any():miss.append(col)
    return miss

def run_bounds_enum_regex(df,schema):
    issues=[]
    for col,spec in schema.items():
        if col not in df:
            issues.append((col,"missing_column"));continue
        s=df[col]
        if "min" in spec and (s<spec["min"]).any():issues.append((col,"min_violation"))
        if "max" in spec and (s>spec["max"]).any():issues.append((col,"max_violation"))
        if "allowed" in spec and (~s.isin(spec["allowed"])).any():issues.append((col,"enum_violation"))
        if "regex" in spec and (~s.astype(str).str.match(spec["regex"],na=True)).any():issues.append((col,"regex_violation"))
    return issues

def evaluate_expr_checks(df, checks, context):
    results = []
    for c in checks or []:
        name = c.get("name", "check")
        expr = c["expr"].replace("@", "")  # remove @ if used
        try:
            res = eval(expr, {}, {"df": df, **context})
            # if expression returns Series → True if all() are True
            if hasattr(res, "all"):
                ok = res.all()
            else:
                ok = bool(res)
            results.append({"name": name, "passed": bool(ok), "expr": expr})
        except Exception as e:
            results.append({"name": name, "passed": False, "error": str(e), "expr": expr})
    return results


