import streamlit as st
import pandas as pd
from datetime import date
from src.database import init_db, add_application, update_application, delete_application, fetch_applications, get_application
from src.analytics import summary_metrics, status_breakdown, monthly_trend, source_breakdown, response_rate
from src.utils import export_csv, validate_application, import_csv

st.set_page_config(page_title="Job Application Tracker", page_icon="💼", layout="wide")

init_db()

st.markdown("""
<style>
.main-title {font-size: 2.2rem; font-weight: 800; margin-bottom: 0.1rem;}
.sub-title {color:#6b7280; margin-bottom:1.4rem;}
.metric-card {padding:18px; border-radius:16px; background:#f8fafc; border:1px solid #e5e7eb;}
.status-pill {padding:4px 9px; border-radius:999px; font-size:12px; font-weight:700;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💼 Job Application Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Track applications, interviews, offers, follow-ups and your complete job-search pipeline.</div>', unsafe_allow_html=True)

apps = fetch_applications()
metrics = summary_metrics(apps)

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total Applications", metrics["total"])
c2.metric("Active", metrics["active"])
c3.metric("Interviews", metrics["interviews"])
c4.metric("Offers", metrics["offers"])
c5.metric("Response Rate", f'{response_rate(apps):.1f}%')

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "➕ Add Application", "📋 Applications", "📥 Import / Export", "⚙️ Manage"])

with tab1:
    st.subheader("Job Search Overview")
    if not apps.empty:
        a,b = st.columns(2)
        with a:
            st.markdown("**Applications by Status**")
            st.bar_chart(status_breakdown(apps), height=300)
        with b:
            st.markdown("**Monthly Applications**")
            st.line_chart(monthly_trend(apps), height=300)
        a,b = st.columns(2)
        with a:
            st.markdown("**Application Sources**")
            st.bar_chart(source_breakdown(apps), height=280)
        with b:
            st.markdown("**Pipeline Snapshot**")
            snapshot = apps.groupby("status").size().sort_values(ascending=False).rename("applications")
            st.dataframe(snapshot, use_container_width=True)
    else:
        st.info("No applications yet. Add your first application to start building your dashboard.")

with tab2:
    st.subheader("Add New Application")
    with st.form("add_form", clear_on_submit=True):
        c1,c2,c3 = st.columns(3)
        company = c1.text_input("Company *")
        role = c2.text_input("Job Role *")
        location = c3.text_input("Location", placeholder="Remote / Bengaluru / Hyderabad")
        c1,c2,c3 = st.columns(3)
        status = c1.selectbox("Status", ["Applied","Screening","Interview","Offer","Rejected","Withdrawn","Ghosted"])
        source = c2.selectbox("Source", ["LinkedIn","Company Website","Naukri","Indeed","Referral","College Placement","Email","Other"])
        applied_date = c3.date_input("Applied Date", value=date.today())
        c1,c2,c3 = st.columns(3)
        job_url = c1.text_input("Job URL")
        salary = c2.text_input("Expected / Listed Salary", placeholder="e.g. ₹6-8 LPA")
        follow_up = c3.date_input("Follow-up Date", value=None)
        notes = st.text_area("Notes", placeholder="Recruiter contact, interview details, preparation notes...")
        submitted = st.form_submit_button("Add Application", type="primary", use_container_width=True)
        if submitted:
            ok, msg = validate_application(company, role)
            if ok:
                add_application(company, role, location, status, source, applied_date, job_url, salary, follow_up, notes)
                st.success("Application added successfully.")
                st.rerun()
            else:
                st.error(msg)

with tab3:
    st.subheader("Application Pipeline")
    if apps.empty:
        st.info("No applications found.")
    else:
        f1,f2,f3,f4 = st.columns(4)
        search = f1.text_input("Search", placeholder="Company or role...")
        statuses = f2.multiselect("Status", sorted(apps["status"].unique()))
        sources = f3.multiselect("Source", sorted(apps["source"].unique()))
        location_filter = f4.text_input("Location")
        filtered = apps.copy()
        if search:
            mask = filtered["company"].str.contains(search, case=False, na=False) | filtered["role"].str.contains(search, case=False, na=False)
            filtered = filtered[mask]
        if statuses:
            filtered = filtered[filtered["status"].isin(statuses)]
        if sources:
            filtered = filtered[filtered["source"].isin(sources)]
        if location_filter:
            filtered = filtered[filtered["location"].str.contains(location_filter, case=False, na=False)]
        st.caption(f"Showing {len(filtered)} of {len(apps)} applications")
        display_cols = ["id","company","role","location","status","source","applied_date","follow_up","salary"]
        st.dataframe(filtered[display_cols].sort_values("applied_date", ascending=False), use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("### Application Details / Edit")
        selected_id = st.selectbox("Select Application ID", filtered["id"].tolist(), format_func=lambda x: f"#{x} — {filtered.loc[filtered.id==x,'company'].iloc[0]} / {filtered.loc[filtered.id==x,'role'].iloc[0]}")
        item = get_application(selected_id)
        if item:
            with st.form("edit_form"):
                c1,c2,c3 = st.columns(3)
                e_company = c1.text_input("Company", value=item["company"])
                e_role = c2.text_input("Job Role", value=item["role"])
                e_location = c3.text_input("Location", value=item["location"] or "")
                c1,c2,c3 = st.columns(3)
                e_status = c1.selectbox("Status", ["Applied","Screening","Interview","Offer","Rejected","Withdrawn","Ghosted"], index=["Applied","Screening","Interview","Offer","Rejected","Withdrawn","Ghosted"].index(item["status"]))
                e_source = c2.selectbox("Source", ["LinkedIn","Company Website","Naukri","Indeed","Referral","College Placement","Email","Other"], index=["LinkedIn","Company Website","Naukri","Indeed","Referral","College Placement","Email","Other"].index(item["source"]))
                e_date = c3.date_input("Applied Date", value=pd.to_datetime(item["applied_date"]).date())
                e_url = st.text_input("Job URL", value=item["job_url"] or "")
                e_salary = st.text_input("Salary", value=item["salary"] or "")
                e_follow = st.date_input("Follow-up Date", value=pd.to_datetime(item["follow_up"]).date() if item["follow_up"] else None)
                e_notes = st.text_area("Notes", value=item["notes"] or "")
                col1,col2 = st.columns(2)
                save = col1.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                remove = col2.form_submit_button("🗑️ Delete Application", use_container_width=True)
                if save:
                    ok,msg = validate_application(e_company,e_role)
                    if ok:
                        update_application(selected_id,e_company,e_role,e_location,e_status,e_source,e_date,e_url,e_salary,e_follow,e_notes)
                        st.success("Application updated.")
                        st.rerun()
                    else: st.error(msg)
                if remove:
                    delete_application(selected_id)
                    st.success("Application deleted.")
                    st.rerun()

with tab4:
    st.subheader("Import / Export Data")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("### Export")
        if not apps.empty:
            csv = export_csv(apps)
            st.download_button("⬇️ Download CSV", csv, "job_applications.csv", "text/csv", use_container_width=True)
        else:
            st.info("Add applications before exporting.")
    with col2:
        st.markdown("### Import")
        uploaded = st.file_uploader("Upload a CSV", type=["csv"])
        if uploaded:
            try:
                imported = import_csv(uploaded)
                st.dataframe(imported.head(10), use_container_width=True)
                if st.button("Import Applications", type="primary"):
                    count = 0
                    for _, r in imported.iterrows():
                        ok,_ = validate_application(str(r.get("company","")), str(r.get("role","")))
                        if ok:
                            add_application(
                                str(r.get("company","")), str(r.get("role","")),
                                str(r.get("location","")), str(r.get("status","Applied")),
                                str(r.get("source","Other")), str(r.get("applied_date",date.today())),
                                str(r.get("job_url","")), str(r.get("salary","")),
                                str(r.get("follow_up","")) if pd.notna(r.get("follow_up","")) else None,
                                str(r.get("notes",""))
                            )
                            count += 1
                    st.success(f"Imported {count} applications.")
                    st.rerun()
            except Exception as e:
                st.error(f"Could not read CSV: {e}")

with tab5:
    st.subheader("Tracker Information")
    st.markdown("""
    **Recommended workflow**
    1. Add every application immediately after applying.
    2. Set a follow-up date for applications that need recruiter outreach.
    3. Update status after every screening/interview.
    4. Export a backup CSV periodically.

    **Data storage:** local SQLite database at `data/jobs.db`. No external account is required.
    """)
    st.code("streamlit run app.py", language="bash")
