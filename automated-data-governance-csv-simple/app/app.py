import os, json, yaml, pandas as pd, numpy as np
import streamlit as st
import plotly.express as px
from utils.io import file_checksum, ensure_dir, now_iso
from governance import schema_registry, validators, pii, lineage

# ---------- SAFE JSON HANDLER ----------
def safe_json_dumps(obj):
    """Safely dump JSON handling pandas/numpy types."""
    def default(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        if isinstance(o, (pd.Timestamp,)): return str(o)
        if isinstance(o, (pd.Series, pd.DataFrame)): return o.to_dict()
        return str(o)
    return json.dumps(obj, indent=2, default=default)

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="CSV Governance Dashboard", page_icon="🛡️", layout="wide")
st.title("🛡️ Automated Data Governance (CSV)")
st.caption("Rule-based validation • PII detection • Schema versioning • Profiling • Curated Output")

# ---------- SIDEBAR ----------
source = st.sidebar.radio("Select Source", ["Upload CSV", "Use Sample"], horizontal=True)
name = st.sidebar.text_input("Dataset name", "orders")
go = st.sidebar.button("🚀 Run Governance", use_container_width=True)

# ---------- LOAD RULES ----------
with open("config/rules.yaml") as f:
    rules = yaml.safe_load(f)

# ---------- LOAD DATA ----------
df, src = None, None
if source == "Upload CSV":
    up = st.file_uploader("Upload CSV file", type=["csv"])
    if up:
        df = pd.read_csv(up)
        ensure_dir("lake/raw")
        src = os.path.join("lake/raw", up.name)
        df.to_csv(src, index=False)
else:
    src = "data/samples/orders.csv"
    df = pd.read_csv(src)

# ---------- GOVERNANCE PIPELINE ----------
if go and df is not None:
    st.markdown("### 📊 Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # ---- Load dataset rules ----
    r = rules["datasets"][name]
    schema = r["schema"]

    # ---- Validation core ----
    df2 = validators.coerce_types(df, schema)
    miss = validators.run_required_checks(df2, schema)
    issues = validators.run_bounds_enum_regex(df2, schema)
    exprs = validators.evaluate_expr_checks(
        df2, r.get("quality_checks"), {"allowed_countries": r.get("allowed_countries", [])}
    )

    # ---- PII detection ----
    find = pii.scan_frame(df2) if r.get("pii_scan") else {}

    # ---- Schema version & lineage ----
    ver = schema_registry.upsert_schema(name, schema)

    # ---- Duplicates check ----
    dup_count = df2.duplicated(subset=[r.get("id_column")], keep=False).sum()
    dup_msg = f"⚠️ Found {dup_count} duplicate records" if dup_count > 0 else "✅ No duplicate records found"

    # ---- Build report object ----
    rep = {
        "dataset": name,
        "rows": len(df2),
        "missing": miss,
        "issues": issues,
        "exprs": exprs,
        "pii": find,
        "duplicates": int(dup_count),
        "ver": ver,
        "ts": now_iso(),
    }

    ensure_dir("reports")
    with open(f"reports/{name}_report.json", "w") as f:
        f.write(safe_json_dumps(rep))

    # ---------- VISUAL SUMMARY ----------
    st.markdown("## 📈 Governance Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows Validated", len(df2))
    c2.metric("Schema Version", ver)
    c3.metric("PII Columns", len(find))
    c4.metric("Duplicates", dup_count)
    st.caption(dup_msg)

    # ---------- PII CHART ----------
    if find:
        pii_counts = {col: len(v) for col, v in find.items()}
        pii_df = pd.DataFrame(list(pii_counts.items()), columns=["Column", "Detections"])
        fig = px.bar(
            pii_df, x="Column", y="Detections", color="Column", text="Detections",
            title="🔐 PII Detection by Column"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No PII detected ✅")

    # ---------- QUALITY CHECKS ----------
    st.markdown("## 🧾 Data Quality Checks")
    qc_df = pd.DataFrame(exprs)
    if not qc_df.empty:
        qc_df["Status"] = qc_df["passed"].map({True: "✅ Passed", False: "❌ Failed"})
        st.dataframe(qc_df[["name", "Status"]], use_container_width=True)
    else:
        st.write("No quality checks defined.")

    # ---------- DATA PROFILING ----------
    st.markdown("## 🧮 Data Profiling Summary")
    profile = df2.describe(include="all").T
    profile["missing_%"] = df2.isna().mean() * 100
    st.dataframe(
        profile[["count", "unique", "top", "freq", "missing_%"]].fillna("-"),
        use_container_width=True
    )

    # ---------- CLEANED DATA OUTPUT ----------
    st.markdown("## 🧹 Curated Clean Data")
    clean_df = df2.dropna(subset=r["schema"].keys())
    ensure_dir("lake/curated")
    clean_path = os.path.join("lake/curated", f"{name}_cleaned.csv")
    clean_df.to_csv(clean_path, index=False)
    st.download_button(
        label="🧹 Download Cleaned CSV",
        data=open(clean_path, "rb").read(),
        file_name=f"{name}_cleaned.csv",
        mime="text/csv",
        use_container_width=True
    )

    # ---------- REPORT DOWNLOAD ----------
    st.markdown("## 📥 Download Governance Report")
    st.download_button(
        label="📥 Download Full Report (JSON)",
        data=safe_json_dumps(rep),
        file_name=f"{name}_governance_report.json",
        mime="application/json",
        use_container_width=True
    )

    # ---------- LINEAGE RECORD ----------
    lineage.record(name, src, file_checksum(src), ver, len(df2), ["validate", "report"])

    st.success("Governance run completed successfully ✅")

    # ---------- RUN HISTORY VIEW ----------
    st.markdown("## 🕒 Run History")
    lineage_path = "metadata/lineage.jsonl"
    if os.path.exists(lineage_path):
        lines = [json.loads(l) for l in open(lineage_path)]
        hist_df = pd.DataFrame(lines)
        if "schema_version" in hist_df.columns:
            hist_df.rename(columns={"schema_version": "ver"}, inplace=True)
        st.dataframe(
            hist_df[["ts", "dataset", "rows", "ver"]].sort_values("ts", ascending=False),
            use_container_width=True
        )
    else:
        st.info("No previous runs found.")

# ---------- DEFAULT PROMPT ----------
elif not go:
    st.info("Upload or use sample, then click **Run Governance** to begin.")
