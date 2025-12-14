# 🎓 Learning Platform API

![Django CI](https://github.com/snushev/learning-platform/workflows/Django%20CI/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![Django Version](https://img.shields.io/badge/django-5.2.8-green.svg)
![DRF Version](https://img.shields.io/badge/DRF-3.16.1-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)


A comprehensive REST API for an online learning platform built with Django REST Framework. Features include course management, student enrollments, quizzes, progress tracking, and course ratings.

## ✨ Features

- 🔐 **Authentication**: JWT-based authentication with role-based access (Students & Instructors)
- 📚 **Course Management**: Create, update, and manage courses with categories and levels
- 📝 **Lessons**: Organize course content with ordered lessons supporting video and text content
- 📊 **Quizzes**: Interactive quizzes with multiple choice and true/false questions
- 🎯 **Enrollments**: Student enrollment system with progress tracking
- ⭐ **Ratings**: Course rating and review system with average rating calculation
- 🚀 **Throttling**: Rate limiting to prevent API abuse
- 📖 **API Documentation**: Interactive Swagger/OpenAPI documentation

## 🛠️ Tech Stack

- **Backend**: Django 5.2.8 + Django REST Framework 3.16.1
- **Database**: PostgreSQL 15
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Web Server**: Nginx (reverse proxy)
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest + pytest-django
- **Code Quality**: Black, Flake8

## 📋 Prerequisites

- Docker & Docker Compose
- Git

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/snushev/learning-platform.git
cd learning-platform
```

### 2. Create environment file
```bash
cp .env.example .env
```

Edit `.env` and set your environment variables.

### 3. Build and run with Docker
```bash
docker-compose up --build
```

### 4. Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the application

- **API Root**: http://localhost/api/
- **Admin Panel**: http://localhost/admin/
- **API Documentation**: http://localhost/api/docs/

## 📚 API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login and get JWT tokens
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/profile/` - Get current user profile
- `PUT /api/users/profile/update/` - Update user profile

### Courses
- `GET /api/courses/` - List all courses (with filtering & search)
- `POST /api/courses/` - Create course (instructors only)
- `GET /api/courses/{id}/` - Get course details
- `PUT /api/courses/{id}/` - Update course (owner only)
- `DELETE /api/courses/{id}/` - Delete course (owner only)

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create category (admin only)

### Lessons
- `GET /api/lessons/` - List lessons
- `GET /api/lessons/?course={id}` - Filter lessons by course
- `POST /api/lessons/` - Create lesson (instructor only)
- `GET /api/lessons/{id}/` - Get lesson details
- `PUT /api/lessons/{id}/` - Update lesson
- `DELETE /api/lessons/{id}/` - Delete lesson

### Enrollments
- `GET /api/enrollments/` - List my enrollments
- `POST /api/enrollments/` - Enroll in a course
- `GET /api/enrollments/{id}/` - Get enrollment details with progress
- `DELETE /api/enrollments/{id}/` - Unenroll from course
- `POST /api/enrollments/{id}/mark-lesson-viewed/` - Mark lesson as viewed

### Quizzes
- `GET /api/quizzes/` - List quizzes
- `GET /api/quizzes/?course={id}` - Filter quizzes by course
- `POST /api/quizzes/` - Create quiz (instructor only)
- `GET /api/quizzes/{id}/` - Get quiz details with questions

### Quiz Attempts
- `GET /api/quiz-attempts/` - List my attempts
- `POST /api/quiz-attempts/` - Start quiz attempt
- `GET /api/quiz-attempts/{id}/` - Get attempt details
- `POST /api/quiz-attempts/{id}/submit/` - Submit quiz answers

### Ratings
- `GET /api/ratings/` - List all ratings
- `GET /api/ratings/?course={id}` - Filter ratings by course
- `POST /api/ratings/` - Rate a course (enrolled students only)
- `PUT /api/ratings/{id}/` - Update rating (owner only)
- `DELETE /api/ratings/{id}/` - Delete rating (owner only)

## 🧪 Running Tests
```bash
# Run all tests
docker-compose exec web pytest

# Run with verbose output
docker-compose exec web pytest -v

# Run specific test file
docker-compose exec web pytest users/tests.py

# Run with coverage
docker-compose exec web pytest --cov=. --cov-report=html
```

## 🔧 Development

### Run locally (without Docker)

1. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up database
```bash
# Start only PostgreSQL container
docker-compose up db

# Run migrations
python manage.py migrate
```

4. Run development server
```bash
python manage.py runserver
```

### Code Quality
```bash
# Format code with Black
black .

# Lint with Flake8
flake8 .
```

## 🔒 Security Features

- JWT token authentication
- Role-based access control (Students & Instructors)
- Rate limiting (100 requests/day for anonymous, 1000/day for authenticated)
- Permission checks on all endpoints
- Unique constraints to prevent duplicate enrollments/ratings

## 📊 Project Structure
```
learning-platform/
├── config/              # Project settings
├── users/               # User authentication & profiles
├── courses/             # Course management
├── lessons/             # Lesson content
├── enrollments/         # Student enrollments & progress
├── quizzes/             # Quiz system
├── ratings/             # Course ratings & reviews
├── nginx/               # Nginx configuration
├── .github/workflows/   # CI/CD pipelines
├── docker-compose.yml   # Docker services
├── Dockerfile           # Django container
├── requirements.txt     # Python dependencies
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Simeon Nushev**
- GitHub: [@snushev](https://github.com/snushev)

## 🙏 Acknowledgments

- Built with Django REST Framework
- API documentation powered by drf-spectacular
- Containerized with Docker

---

Made with ❤️ by Simeon Nushev
