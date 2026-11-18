# KAABIL — Career Intelligence Platform

A bright, responsive Django starter platform for student career exploration, skill-gap awareness, quizzes, learning tasks, resume keyword review and opportunity discovery.

## What's included

- Bright white / soft-blue responsive landing page and workspace.
- Django signup, login and logout.
- Student profile.
- Career roles and transparent rule-based matching.
- Skill-gap comparison.
- Weekly task checklist.
- Multiple-choice quiz and answer history.
- PDF/DOCX resume text extraction and basic keyword coverage estimate.
- Job listings with demo labels.
- Django admin for managing starter content.
- SQLite local development; PostgreSQL through `DATABASE_URL`.
- Starter data management command and basic scoring tests.

## Important scope notes

This is a functional starter implementation, not a fully audited production service.
- Career matching uses a transparent weighted rule, not a trained predictive ML model.
- Resume score is a basic keyword coverage estimate, not an official ATS score.
- Job entries created by the seed command are demo listings, not live vacancies.
- Learning tasks are managed through Django admin in this starter version.
- No third-party live job API is configured.
- Before public launch, complete security review, privacy/legal review, accessibility testing, backups, monitoring and production deployment configuration.

## Requirements

- Python 3.10+
- Internet connection for Google Fonts and Bootstrap CDN (or self-host those assets for offline use).

## Windows setup

Open Command Prompt or VS Code terminal inside the extracted `KAABIL` folder:

```bat
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
py manage.py makemigrations core
py manage.py migrate
py manage.py seed_kaabil
py manage.py createsuperuser
py manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## macOS / Linux setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_kaabil
python manage.py createsuperuser
python manage.py runserver
```

## PostgreSQL

Set `DATABASE_URL` in `.env`, for example:

```env
DATABASE_URL=postgresql://kaabil_user:your_password@localhost:5432/kaabil_db
```

Create the database and user in PostgreSQL before running migrations. Keep `.env` private and never commit it.

## First-time content setup

1. Register a student account on `/signup/`.
2. Create a superuser using `createsuperuser`.
3. Visit `/admin/`.
4. Add `StudentSkill` records for a student and select levels from 0 to 100.
5. Add `LearningTask` records for students.
6. Add quiz questions as needed.
7. Explore career matching and skill gaps.

The seed command creates 10 career roles, starter skill requirements, one quiz question and two clearly labelled demo job listings:

```bash
python manage.py seed_kaabil
```

## Tests and checks

```bash
python manage.py check
python manage.py test core
```

## Project structure

```text
KAABIL/
├── config/                 # Django settings and URL configuration
├── core/                   # Models, views, forms, scoring, admin and tests
├── frontend/
│   ├── templates/          # Landing, auth and workspace pages
│   └── static/             # CSS and JavaScript
├── media/                  # Uploaded resumes (created at runtime)
├── manage.py
├── requirements.txt
└── .env.example
```

## Production checklist

- Set a strong random `DJANGO_SECRET_KEY`.
- Set `DJANGO_DEBUG=False`.
- Set exact `DJANGO_ALLOWED_HOSTS`.
- Configure PostgreSQL and backups.
- Configure HTTPS and secure cookies.
- Use private/object storage for uploads and enforce retention policies.
- Add rate limiting, audit logging and monitoring.
- Review privacy notice, consent, data deletion and retention.
- Add comprehensive tests and run a security review.
- Configure a real job provider only after checking its terms and credentials.
