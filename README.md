### Group Members

| S/N | Full Name | Registration Number |
| :--- | :--- | :--- |
| 1 | RAYMOND LUMWA MATHEW | 33393/T.2024 |
| 2 | ASHIRAFU ADOFU ALIFA | 34736/T.2024 |
| 3 | GLADNESS JUMANNE TEMBO | 34552/T.2024 |
| 4 | SEIF SHABAN MAFURU | 34436/T.2024 |
| 5 | LUCAS JUSTUS NGIMBWA | 33469/T.2024 |
| 6 | DANIEL ERASMO NCHASI | 32267/T.2023 |
| 7 | ATHUMAN HASSAN MGONJA | 34511/T.2024 |
| 8 | EDIGA EDWINE KASHUKU | 33634/T.2024 |
| 9 | FESTO METHOD DUKENYE | 34144/T.2024 |
| 10 | ELIUD KIMAMBO EBENEZERY | 33598/T.2024 |


# NGO Volunteer Management System

A full-featured Django application for NGOs to recruit, manage, and track volunteers.
It supports three roles — **Volunteers**, **Organization Admins**, and **System Admins** —
each with their own dashboard and permissions.

## Features

- **Custom user model** with role-based access (`volunteer`, `org_admin`, `admin`)
- **Volunteer signup & profiles**: skills, availability, interests, emergency contact, auto-calculated badge level (Bronze/Silver/Gold based on approved hours)
- **Organization signup & profiles**: description, mission, logo, contact info; new orgs start unverified and must be approved by a System Admin
- **Opportunities (events/listings)**: organizations create/edit/publish opportunities with dates, location or remote flag, required skills, category, and volunteer capacity
- **Applications**: volunteers browse & search opportunities and apply; organizations approve/reject applications; capacity is enforced automatically
- **Hour logging & approval**: volunteers log hours against opportunities they were approved for; organizations approve/reject submitted hours
- **Dashboards**:
  - Volunteer dashboard — approved hours, badge level, recent applications, recommended opportunities
  - Organization dashboard — stats, pending applications, pending hour approvals
  - System Admin dashboard — platform-wide stats, organization verification queue
- **Django Admin** fully wired up for all models (`/admin/`)
- Bootstrap 5 responsive UI

## Project Structure

```
config/            # project settings, root urls
accounts/          # custom User model, auth, profile
organizations/     # Organization model & views
volunteers/        # VolunteerProfile, Skill
opportunities/     # Opportunity, Category (the "events")
applications/       # Volunteer applications to opportunities
hours/             # Volunteer hour logs & approval
dashboard/         # Role-based dashboard routing
templates/          # All HTML templates (Bootstrap 5)
static/            # CSS
```

## Setup

1. **Create a virtual environment and install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py migrate
   ```

3. **Create a System Admin (superuser)**
   ```bash
   python manage.py createsuperuser
   ```
   Logging in with this account automatically routes to the System Admin dashboard,
   and it can also access the full Django admin at `/admin/`.

4. **Run the development server**
   
   python manage.py runserver
   
   Visit `http://127.0.0.1:8000/`.

## Typical Workflow

1. An **organization** signs up at `/accounts/signup/organization/` — its account starts unverified.
2. A **System Admin** verifies it from the Admin Dashboard (or `/admin/`).
3. The **org admin** edits its organization profile and creates opportunities
   (`/opportunities/create/`), publishing them when ready.
4. A **volunteer** signs up at `/accounts/signup/volunteer/`, fills in skills/availability,
   browses opportunities, and applies.
5. The **org admin** reviews and approves/rejects applications from the opportunity's
   "Review Applications" page.
6. Once approved, the **volunteer** can log hours against that opportunity (`/hours/log/`).
7. The **org admin** approves submitted hours (`/hours/pending/`), which count toward
   the volunteer's total and badge level.

## Configuration Notes

- Uses SQLite by default (zero config). Swap `DATABASES` in `config/settings.py` for
  Postgres/MySQL in production.
- `DEBUG`, `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS` can be set via environment
  variables — **change the secret key and set `DEBUG=False` before deploying**.
- Uploaded images (profile pictures, org logos) are stored under `media/`.
- For production, run `python manage.py collectstatic` and serve `static/`/`media/`
  via your web server or a service like WhiteNoise/S3.

## Extending

Natural next additions if you want to keep building:
- Email notifications (application approved, hours approved, etc.) via `django.core.mail`
- PDF volunteer certificates using the hours skill data
- REST API (Django REST Framework) for a mobile app
- Calendar/ICS export for opportunity dates
- Volunteer-opportunity skill matching score on the recommendations list
