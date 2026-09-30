import pandas as pd
from io import BytesIO

REQUIRED = ["company", "role"]

def validate_application(company, role):
    if not company or not company.strip():
        return False, "Company name is required."
    if not role or not role.strip():
        return False, "Job role is required."
    return True, ""

def export_csv(df):
    cols = ["company","role","location","status","source","applied_date","job_url","salary","follow_up","notes"]
    return df[[c for c in cols if c in df.columns]].to_csv(index=False).encode("utf-8")

def import_csv(uploaded_file):
    data = pd.read_csv(uploaded_file)
    data.columns = [str(c).strip().lower() for c in data.columns]
    for col in ["company","role"]:
        if col not in data.columns:
            raise ValueError(f"CSV must contain '{col}' column.")
    defaults = {
        "location":"", "status":"Applied", "source":"Other", "applied_date":pd.Timestamp.today().date(),
        "job_url":"", "salary":"", "follow_up":"", "notes":""
    }
    for col,val in defaults.items():
        if col not in data.columns:
            data[col] = val
    return data
