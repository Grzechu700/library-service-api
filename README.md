# Library Service API

A comprehensive library management system built with Django REST Framework. This API provides endpoints for managing books, user authentication, and borrowing operations with automatic inventory tracking.

## Features

### Core Functionality
- **Books Management**: Full CRUD operations for books with cover type enum (HARD/SOFT)
- **User Authentication**: JWT-based authentication with custom `Authorize` header
- **Borrowing System**: 
  - Create borrowings with automatic inventory decrease
  - Return books with automatic inventory increase
  - Track borrow dates and return dates
- **Advanced Filtering**: Filter borrowings by active status and user
- **Permissions**: Admin-only write access to books, user-specific borrowing views

### Custom Endpoints
- `POST /api/borrowings/{id}/return/` - Return a borrowed book (sets actual_return_date, increases inventory)
- `GET /api/borrowings/?is_active=true` - Filter active/returned borrowings
- `GET /api/borrowings/?user_id={id}` - Admin-only: filter borrowings by user

## Technologies

- **Python 3.12+**
- **Django 6.0**
- **Django REST Framework 3.15**
- **PostgreSQL 16**
- **JWT Authentication** (djangorestframework-simplejwt)
- **API Documentation** (drf-spectacular)
- **Testing** (pytest, pytest-django, pytest-cov)

## Installation

### Prerequisites
- Python 3.12 or higher
- PostgreSQL 16
- Git

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd library-service-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL database**
```sql
CREATE DATABASE library_service_db;
```

5. **Configure environment variables**
Create `.env` file in project root:
```env
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
DATABASE_NAME=library_service_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Run development server**
```bash
python manage.py runserver
```

API will be available at `http://127.0.0.1:8000/`

## API Documentation

### Swagger UI
Interactive API documentation: `http://127.0.0.1:8000/api/doc/swagger/`

### ReDoc
Alternative documentation: `http://127.0.0.1:8000/api/doc/redoc/`

### OpenAPI Schema
Raw schema: `http://127.0.0.1:8000/api/schema/`

## Authentication

This API uses JWT authentication with a **custom header**:

**Header:** `Authorize: Bearer <your-token>`

**Note:** Standard `Authorization` header is NOT used. Use `Authorize` instead.

### Obtaining Tokens

**Endpoint:** `POST /api/users/token/`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response:**
Returns `access` and `refresh` JWT tokens for authentication.

## Running Tests

### Run all tests with coverage
```bash
pytest
```

### Run specific test file
```bash
pytest books/test_permissions.py
```

### Generate HTML coverage report
```bash
pytest --cov-report=html
```
View report: `htmlcov/index.html`

### Current Test Coverage
- **Overall**: 87% (exceeds 60% requirement)
- **Views**: 100%
- **Serializers**: 96%

## API Endpoints

### Books
- `GET /api/books/` - List all books (public)
- `POST /api/books/` - Create book (admin only)
- `GET /api/books/{id}/` - Retrieve book details (public)
- `PUT /api/books/{id}/` - Update book (admin only)
- `PATCH /api/books/{id}/` - Partial update (admin only)
- `DELETE /api/books/{id}/` - Delete book (admin only)

### Users
- `POST /api/users/register/` - Register new user
- `POST /api/users/token/` - Obtain JWT token
- `POST /api/users/token/refresh/` - Refresh JWT token
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update current user profile

### Borrowings
- `GET /api/borrowings/` - List user's borrowings (all for admin)
- `POST /api/borrowings/` - Create new borrowing
- `GET /api/borrowings/{id}/` - Retrieve borrowing details
- `POST /api/borrowings/{id}/return/` - **Custom: Return borrowed book**

#### Borrowing Filters
- `?is_active=true` - Show only active borrowings (not returned)
- `?is_active=false` - Show only returned borrowings
- `?user_id={id}` - Filter by user (admin only)

## Project Structure
```
library-service-api/
├── books/                  # Books app
│   ├── migrations/
│   ├── models.py          # Book model with cover enum
│   ├── serializers.py     # Book serializers
│   ├── views.py           # Book viewset with permissions
│   ├── permissions.py     # IsAdminOrReadOnly permission
│   └── test_permissions.py
├── users/                  # Users app
│   ├── migrations/
│   ├── models.py          # Custom User model (email-based)
│   ├── serializers.py     # User & auth serializers
│   └── views.py           # User registration & profile
├── borrowings/             # Borrowings app
│   ├── migrations/
│   ├── models.py          # Borrowing model with constraints
│   ├── serializers.py     # Read & Create serializers
│   ├── views.py           # Borrowing viewset with filters
│   ├── test_borrowing.py
│   └── test_filtering.py
├── library_service/        # Project settings
│   ├── settings.py
│   └── urls.py
├── conftest.py            # Pytest fixtures
├── pytest.ini             # Pytest configuration
├── requirements.txt
└── README.md
```

## Key Features Implementation

### Inventory Management
- **Automatic decrease** when borrowing is created
- **Automatic increase** when book is returned
- **Validation** prevents borrowing when inventory is 0

### Date Constraints
- `expected_return_date` must be after `borrow_date`
- `actual_return_date` must be after or equal to `borrow_date`
- Constraints enforced at database level

### Permissions
- **Books**: Public read, admin write
- **Borrowings**: Authenticated users only
- **User Filtering**: Admin can see all users' borrowings
- **Regular Users**: Can only see their own borrowings

### Custom Return Endpoint
```python
POST /api/borrowings/{id}/return/
```
- Sets `actual_return_date` to current date
- Increases book inventory by 1
- Validates borrowing is not already returned
- Returns updated borrowing with nested book details

## License

This project is part of a Django REST Framework bootcamp assessment.