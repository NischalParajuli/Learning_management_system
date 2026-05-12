# Learning Management System (LMS)

A production-oriented Learning Management System built with Django REST Framework, PostgreSQL, Celery, and Redis.

This project supports multiple user roles including Admins, Instructors, Students, and Sponsors, while providing course management, assessments, sponsorship workflows, analytics dashboards, JWT authentication, and automated email reminders.

---

# Features

## Authentication & Authorization

* JWT-based authentication using SimpleJWT
* Role-based access control using custom DRF permissions
* Separate permissions for Admins, Instructors, Students, and Sponsors
* Protected API endpoints

## Course Management

* Create, update, publish, and manage courses
* Difficulty-based course categorization
* Course enrollment system
* Course progress tracking
* Pagination, filtering, searching, and ordering

## Assessments System

* Assignment creation and management
* Student assignment submissions
* Instructor grading and feedback system
* Submission deadline validation
* Quiz and question management
* Student quiz submissions and score tracking

## Sponsorship System

* Sponsor individual student enrollments
* Sponsor entire courses
* Sponsorship progress tracking
* Funding and sponsorship analytics

## Dashboards & Analytics

### Admin Dashboard

* Total users
* Total students, instructors, and sponsors
* Active courses
* Enrollment statistics
* Assignment statistics
* Sponsorship analytics

### Sponsor Dashboard

* Sponsored students overview
* Sponsorship impact tracking
* Student progress monitoring
* Funding utilization insights

## Email Notification System

* Automated assignment reminder emails
* Course ending notifications
* Reminder logging system
* Celery Beat scheduled tasks
* Redis-backed background task processing

## Home Page

* Responsive home page for quick platform overview
* Landing page accessible to all users
* Easy navigation to key platform features

## API Features

* RESTful API architecture
* Swagger/OpenAPI documentation
* ReDoc documentation
* Filtering and searching
* Pagination support
* Structured serializers and validations

---

# Tech Stack

## Backend

* Python 3.14
* Django 6.0
* Django REST Framework

## Database

* PostgreSQL

## Authentication

* SimpleJWT

## Background Tasks

* Celery
* Celery Beat
* Redis

## API Documentation

* drf-spectacular
* Swagger UI
* ReDoc

## Additional Tools

* django-filter
* Django Email Backend

---

# System Architecture

```text
Client Request
      ↓
Django REST Framework APIs
      ↓
Business Logic Layer
      ↓
PostgreSQL Database
      ↓
Celery + Redis Background Tasks
      ↓
Email Notifications & Scheduled Jobs
```

---

# User Roles

## Admin

* Full platform access
* Manage users and courses
* Access analytics dashboard
* Manage sponsorships
* Monitor enrollments and submissions

## Instructor

* Create and manage courses
* Create assignments and quizzes
* Grade student submissions
* Monitor student performance

## Student

* Enroll in courses
* Submit assignments
* Attempt quizzes
* Track progress and grades

## Sponsor

* Sponsor students or courses
* Track sponsored student progress
* Monitor funding impact and utilization

---

# Installation

## Prerequisites

* Python 3.10+
* PostgreSQL
* Redis
* pip
* Virtual Environment

---

## 1. Clone Repository

```bash
git clone <repository-url>
cd Learning_management_system
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure PostgreSQL

Create a PostgreSQL database and update database settings in:

```text
learning/settings.py
```

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lms_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 5. Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password

CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

---

## 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 7. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 8. Start Development Server

```bash
python manage.py runserver
```

---

## 9. Start Redis

```bash
redis-server
```

---

## 10. Start Celery Worker

```bash
celery -A learning worker -l info
```

---

## 11. Start Celery Beat

```bash
celery -A learning beat -l info
```

---

# API Documentation

## Swagger UI

```text
http://127.0.0.1:8000/api/docs/
```

## ReDoc

```text
http://127.0.0.1:8000/api/redoc/
```

## OpenAPI Schema

```text
http://127.0.0.1:8000/api/schema/
```

---

# Authentication

## Register User

```http
POST /api/register/
```

## Login User

```http
POST /api/login/
```

## Refresh JWT Token

```http
POST /api/token/refresh/
```

---

# API Endpoints

## Courses

| Method | Endpoint            | Description      |
| ------ | ------------------- | ---------------- |
| GET    | `/api/course/`      | List all courses |
| POST   | `/api/course/`      | Create course    |
| GET    | `/api/course/{id}/` | Retrieve course  |
| PUT    | `/api/course/{id}/` | Update course    |
| DELETE | `/api/course/{id}/` | Delete course    |

### Course Features

* Search by title, instructor, and difficulty
* Filter by difficulty and publish status
* Ordering and pagination support

---

## Assignments

| Method | Endpoint                            | Description       |
| ------ | ----------------------------------- | ----------------- |
| GET    | `/api/assesments/assignments/`      | List assignments  |
| POST   | `/api/assesments/assignments/`      | Create assignment |
| PUT    | `/api/assesments/assignments/{id}/` | Update assignment |
| DELETE | `/api/assesments/assignments/{id}/` | Delete assignment |

---

## Home Page

| Method | Endpoint               | Description                          |
| ------ | ---------------------- | ------------------------------------ |
| GET    | `/api/assesments/`     | View home page (HTML template)       |

---

## Submissions

| Method | Endpoint                            | Description       |
| ------ | ----------------------------------- | ----------------- |
| GET    | `/api/assesments/submissions/`      | List submissions  |
| POST   | `/api/assesments/submissions/`      | Submit assignment |
| PUT    | `/api/assesments/submissions/{id}/` | Update submission |
| DELETE | `/api/assesments/submissions/{id}/` | Delete submission |

---

## Sponsorships

| Method | Endpoint                             | Description        |
| ------ | ------------------------------------ | ------------------ |
| GET    | `/api/sponsorship/sponsorship/`      | List sponsorships  |
| POST   | `/api/sponsorship/sponsorship/`      | Create sponsorship |
| PUT    | `/api/sponsorship/sponsorship/{id}/` | Update sponsorship |
| DELETE | `/api/sponsorship/sponsorship/{id}/` | Delete sponsorship |

---

## Dashboard

| Method | Endpoint                | Description               |
| ------ | ----------------------- | ------------------------- |
| GET    | `/api/admin-dashboard/` | Admin analytics dashboard |

---

# Sample Dashboard Response

```json
{
  "users": {
    "total_users": 120,
    "students": 90,
    "instructors": 12,
    "sponsors": 18
  },
  "courses": {
    "total_courses": 15,
    "active_courses": 10
  },
  "enrollments": {
    "total_enrollments": 340,
    "active_enrollments": 250
  }
}
```

---

# Project Structure

```text
Learning_management_system/
│
├── learning/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── asgi.py
│
├── accounts/
│   ├── models.py
│   ├── serializer.py
│   ├── permissions.py
│   └── views.py
│
├── courses/
│   ├── models.py
│   ├── serializer.py
│   ├── views.py
│   └── pagination.py
│
├── assesments/
│   ├── models.py
│   ├── serializer.py
│   ├── services.py
│   ├── tasks.py
│   └── views.py
│
├── sponsorship/
│   ├── models.py
│   ├── serializer.py
│   └── views.py
│
├── dashboard/
│   ├── views.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# Key Backend Concepts Demonstrated

* REST API Design
* JWT Authentication
* Role-Based Access Control
* DRF ViewSets & APIViews
* Serializer Validation
* PostgreSQL Integration
* Celery Background Tasks
* Redis Integration
* Scheduled Email Automation
* Pagination, Filtering, and Search
* Analytics & Aggregation Queries
* Service Layer Architecture
* Permission-Based Querysets

---

# Future Improvements

* Docker containerization
* CI/CD pipeline integration
* Real-time notifications using WebSockets
* Payment gateway integration
* Course recommendation system
* File uploads using cloud storage
* Redis caching optimization
* Frontend integration with React or Next.js
* Advanced analytics and reporting charts

---

# Troubleshooting

## Migration Issues

```bash
python manage.py makemigrations
python manage.py migrate
```

## Celery Not Running

* Ensure Redis server is running
* Verify Celery broker URL
* Restart Celery worker and beat

## Email Not Sending

* Verify SMTP credentials
* Check Mailtrap configuration
* Review Django logs

---

# License

This project is licensed under the MIT License.

---

# Author

Developed as a backend-focused LMS project using Django REST Framework, PostgreSQL, Celery, and Redis.

---

# Last Updated

May 2026
