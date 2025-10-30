
import re
EMAIL=re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE=re.compile(r"\+?\d[\d\-\s]{7,}\d")
PAN=re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")
CREDIT=re.compile(r"\b(?:\d[ -]*?){13,16}\b")

def scan_value(v):
    hits=[]
    if not isinstance(v,str):return hits
    if EMAIL.search(v):hits.append("email")
    if PHONE.search(v):hits.append("phone")
    if PAN.search(v):hits.append("pan_like")
    if CREDIT.search(v):hits.append("credit_card_like")
    return hits

def scan_frame(df):
    findings={}
    for col in df.columns:
        flags=set()
        for val in df[col].astype(str).head(1000):
            for k in scan_value(val):flags.add(k)
        if flags:findings[col]=list(flags)
    return findings
