# 💼 Job Application Tracker

A strong portfolio-ready job application management dashboard built with **Python, Streamlit, SQLite and Pandas**.

## Features

- SQLite persistent database
- Add, edit and delete applications
- Application pipeline with statuses
- Search and multi-filter applications
- Dashboard KPIs
- Status, source and monthly analytics
- Follow-up date tracking
- Salary and job URL fields
- Notes for recruiter/interview information
- CSV import
- CSV export
- Responsive Streamlit interface
- No external database or API key required

## Tech Stack

- Python 3.10+
- Streamlit
- Pandas
- SQLite

## Project Structure

```text
Job_Application_Tracker/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── analytics.py
│   └── utils.py
└── sample_data/
    └── applications.csv
```

## Windows Setup

```powershell
cd "Job_Application_Tracker"
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Optional sample data

Use `sample_data/applications.csv` with the Import / Export tab.

## Database

The application automatically creates:

```text
data/jobs.db
```

The database is local and persistent.

## Portfolio Highlights

This project demonstrates:

- CRUD application development
- Relational database design
- Data analytics
- Dashboard development
- Search and filtering
- CSV data pipelines
- Form validation
- Modular Python architecture
- Business-oriented UI/UX

## Future Enhancements

- User authentication
- Resume attachment storage
- Email reminders
- Calendar integration
- Kanban board
- Interview question tracker
- AI resume-job matching
- PostgreSQL deployment
