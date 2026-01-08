# Me-API Playground

A single-user profile API built with Django REST Framework for an internship assessment.

## 📋 Project Overview

Me-API Playground is a simple REST API that allows you to manage a personal profile, projects, and skills. It's designed to demonstrate backend development skills with Django and Django REST Framework.

**Key Features:**
- Single-user profile management (no authentication)
- Projects with associated skills
- Search functionality across profiles, skills, and projects
- Top skills ranking by project count
- Health check endpoint for deployment monitoring

## 🏗️ Architecture

```
me_api/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── me_api/                   # Django project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # Root URL routing
│   └── wsgi.py              # WSGI entry point
└── profiles/                 # Main application
    ├── models.py            # Database models
    ├── serializers.py       # DRF serializers
    ├── views.py             # API views
    ├── urls.py              # API URL patterns
    ├── admin.py             # Admin configuration
    └── management/
        └── commands/
            └── seed_data.py # Sample data command
```

## 📊 Database Schema

### Profile
| Field      | Type         | Description                    |
|------------|--------------|--------------------------------|
| id         | BigAutoField | Primary key                    |
| name       | CharField    | Full name                      |
| email      | EmailField   | Email address                  |
| education  | TextField    | Education background           |
| work       | TextField    | Work experience                |
| github     | URLField     | GitHub profile URL             |
| linkedin   | URLField     | LinkedIn profile URL           |
| portfolio  | URLField     | Portfolio website URL          |
| skills     | M2M          | Many-to-Many with Skill        |
| projects   | M2M          | Many-to-Many with Project      |

### Skill
| Field | Type         | Description         |
|-------|--------------|---------------------|
| id    | BigAutoField | Primary key         |
| name  | CharField    | Skill name (unique) |

### Project
| Field       | Type         | Description                    |
|-------------|--------------|--------------------------------|
| id          | BigAutoField | Primary key                    |
| title       | CharField    | Project title                  |
| description | TextField    | Project description            |
| links       | JSONField    | Links (github, demo, etc.)     |
| skills      | M2M          | Many-to-Many with Skill        |

### Relationships
- Profile ↔ Skill: Many-to-Many
- Profile ↔ Project: Many-to-Many
- Project ↔ Skill: Many-to-Many

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd me_api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Seed sample data (optional)**
   ```bash
   python manage.py seed_data
   ```

6. **Create superuser for admin access (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## 📖 API Documentation

### Endpoints

| Method | Endpoint             | Description                          |
|--------|----------------------|--------------------------------------|
| GET    | `/health`            | Health check                         |
| POST   | `/api/profile`       | Create profile                       |
| GET    | `/api/profile`       | Get profile                          |
| PUT    | `/api/profile`       | Update profile                       |
| GET    | `/api/projects`      | List all projects                    |
| GET    | `/api/projects?skill=<name>` | Filter projects by skill    |
| GET    | `/api/skills/top`    | Get skills ordered by project count  |
| GET    | `/api/search?q=<query>` | Search across profile, skills, projects |

### API Examples (curl)

#### Health Check
```bash
curl http://127.0.0.1:8000/health
```
Response:
```json
{"status": "ok"}
```

#### Create Profile
```bash
curl -X POST http://127.0.0.1:8000/api/profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "education": "B.S. Computer Science",
    "work": "Software Engineer at Tech Co",
    "github": "https://github.com/janedoe",
    "linkedin": "https://linkedin.com/in/janedoe",
    "portfolio": "https://janedoe.dev",
    "skill_names": ["Python", "Django", "React"]
  }'
```

#### Get Profile
```bash
curl http://127.0.0.1:8000/api/profile
```

#### Update Profile
```bash
curl -X PUT http://127.0.0.1:8000/api/profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "skill_names": ["Python", "Django", "React", "Docker"]
  }'
```

#### Get All Projects
```bash
curl http://127.0.0.1:8000/api/projects
```

#### Filter Projects by Skill
```bash
curl "http://127.0.0.1:8000/api/projects?skill=Python"
```

#### Get Top Skills
```bash
curl http://127.0.0.1:8000/api/skills/top
```
Response:
```json
[
  {"id": 1, "name": "Python", "project_count": 3},
  {"id": 2, "name": "Django", "project_count": 2},
  {"id": 3, "name": "React", "project_count": 1}
]
```

#### Search
```bash
curl "http://127.0.0.1:8000/api/search?q=python"
```
Response:
```json
{
  "query": "python",
  "results": {
    "profiles": [],
    "skills": [{"id": 1, "name": "Python"}],
    "projects": [{"id": 1, "title": "Python Web Scraper", "description": "..."}]
  }
}
```

## 🌐 Deployment on Render

### Quick Deploy

1. Push your code to GitHub

2. Create a new **Web Service** on [Render](https://render.com)

3. Connect your GitHub repository

4. Configure the service:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn me_api.wsgi:application`

5. Add environment variables:
   - `DJANGO_SECRET_KEY`: Generate a secure secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Render domain (e.g., `your-app.onrender.com`)

### Environment Variables

| Variable              | Description                              |
|-----------------------|------------------------------------------|
| `DJANGO_SECRET_KEY`   | Django secret key (required in production) |
| `DEBUG`               | Set to `False` in production             |
| `ALLOWED_HOSTS`       | Comma-separated list of allowed hosts    |

## ⚠️ Known Limitations

1. **Single User Only**: This API is designed for a single user. Only one profile can exist at a time.

2. **No Authentication**: The API has no authentication or authorization. Anyone can read/write data.

3. **SQLite Database**: Uses SQLite which is not recommended for production with high traffic. For production, consider PostgreSQL.

4. **No Pagination**: API responses are not paginated. Large datasets may cause performance issues.

5. **No Rate Limiting**: No rate limiting is implemented.

6. **No Input Validation**: Minimal input validation beyond Django's built-in field validators.

## 📄 Resume

[📎 Link to my resume](#) <!-- Replace with your actual resume link -->

## 📝 License

This project is for educational/assessment purposes.

---

Built with ❤️ using Django REST Framework
