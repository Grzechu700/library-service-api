# Library Service API

A comprehensive library management system built with Django REST Framework. This API provides endpoints for managing books, user authentication, borrowing operations with automatic inventory tracking, and payment processing.

## Features

### Core Functionality
- **Books Management**: Full CRUD operations for books with cover type enum (HARD/SOFT)
- **User Authentication**: JWT-based authentication with custom `Authorize` header
- **Borrowing System**: 
  - Create borrowings with automatic inventory decrease
  - Return books with automatic inventory increase
  - Track borrow dates and return dates
- **Payment System**:
  - Track payments for borrowings
  - Support for regular payments and fines
  - Payment status tracking (PENDING/PAID)
  - Filter payments by status and type
- **Advanced Filtering**: Filter borrowings by active status and user
- **Permissions**: Admin-only write access to books, user-specific borrowing views
- **Docker Support**: Full containerization with docker-compose

### Custom Endpoints
- `POST /api/borrowings/{id}/return/` - Return a borrowed book (sets actual_return_date, increases inventory)
- `GET /api/borrowings/?is_active=true` - Filter active/returned borrowings
- `GET /api/borrowings/?user_id={id}` - Admin-only: filter borrowings by user
- `POST /api/payments/{id}/mark_paid/` - Mark payment as paid
- `GET /api/payments/my_payments/` - Get authenticated user's payments
- `GET /api/payments/pending/` - Get all pending payments

## Technologies

- **Python 3.14**
- **Django 6.0**
- **Django REST Framework 3.15**
- **PostgreSQL 16**
- **JWT Authentication** (djangorestframework-simplejwt)
- **API Documentation** (drf-spectacular)
- **Testing** (pytest, pytest-django, pytest-cov)
- **Docker & Docker Compose**

## Installation

### Prerequisites
- Docker & Docker Compose (recommended)
- OR: Python 3.12+, PostgreSQL 16, Git (for local setup)

### Option 1: Docker Setup (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd library-service-api
```

2. **Start with Docker Compose**
```bash
docker-compose up --build
```

That's it! The application will be available at `http://localhost:8000`

Docker will automatically:
- Set up PostgreSQL database
- Run migrations
- Collect static files
- Start the development server

### Option 2: Local Setup

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
Create `.env` file in project root (see `.env.sample` for template):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=library_service_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
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

## Docker Commands (Makefile)

The project includes a Makefile for convenient Docker operations:
```bash
make help       # Show all available commands
make build      # Build Docker images
make up         # Start all services in detached mode
make down       # Stop all services
make restart    # Restart all services
make logs       # Show logs (follow mode)
make shell      # Open Django shell in container
make migrate    # Run migrations in container
make test       # Run tests in container
make clean      # Remove containers and volumes
```

Or use docker-compose directly:
```bash
docker-compose up          # Start services (attached)
docker-compose up -d       # Start services (detached)
docker-compose down        # Stop services
docker-compose logs -f     # View logs
docker-compose exec web python manage.py createsuperuser  # Create superuser
```

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

**Response:** Returns `access` and `refresh` JWT tokens for authentication.

## Running Tests

### Local Environment
```bash
pytest
```

### Docker Environment
```bash
docker-compose exec web pytest
# OR
make test
```

### Generate Coverage Report
```bash
pytest --cov-report=html
```
View report: `htmlcov/index.html`

### Current Test Coverage
- **Overall**: 83% (exceeds 60% requirement)
- **13 comprehensive tests**
- **Views**: High coverage on custom functionality
- **Serializers**: Validation and business logic tested

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

### Payments
- `GET /api/payments/` - List payments (user's own or all for admin)
- `GET /api/payments/{id}/` - Payment details
- `POST /api/payments/` - Create payment
- `POST /api/payments/{id}/mark_paid/` - Mark payment as paid
- `GET /api/payments/my_payments/` - Get user's payments
- `GET /api/payments/pending/` - Get pending payments

#### Payment Filters
- `?status=PENDING` - Filter by status (PENDING/PAID)
- `?type=PAYMENT` - Filter by type (PAYMENT/FINE)

## Project Structure
```
library-service-api/
├── books/                  # Books app
│   ├── migrations/
│   ├── models.py          # Book model with cover enum
│   ├── serializers.py     # Book serializers
│   ├── views.py           # Book viewset with permissions
│   ├── permissions.py     # IsAdminOrReadOnly permission
│   └── urls.py
├── users/                  # Users app
│   ├── migrations/
│   ├── models.py          # Custom User model (email-based)
│   ├── serializers.py     # User & auth serializers
│   ├── views.py           # User registration & profile
│   └── urls.py
├── borrowings/             # Borrowings app
│   ├── migrations/
│   ├── models.py          # Borrowing model with constraints
│   ├── serializers.py     # Read & Create serializers
│   ├── views.py           # Borrowing viewset with filters
│   └── urls.py
├── payments/               # Payments app
│   ├── migrations/
│   ├── models.py          # Payment model
│   ├── serializers.py     # Payment serializers
│   ├── views.py           # Payment viewset
│   └── urls.py
├── tests/                  # Centralized tests directory
│   ├── conftest.py        # Pytest fixtures
│   ├── test_books_permissions.py
│   ├── test_borrowings.py
│   └── test_borrowings_filtering.py
├── library_service/        # Project settings
│   ├── settings.py
│   └── urls.py
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker services configuration
├── entrypoint.sh         # Docker startup script
├── Makefile              # Convenient Docker commands
├── pytest.ini            # Pytest configuration
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
- Constraints enforced at database level with validation at serializer level

### Permissions
- **Books**: Public read, admin write
- **Borrowings**: Authenticated users only
- **Payments**: Users see only their own, admins see all
- **User Filtering**: Admin can see all users' borrowings
- **Regular Users**: Can only see their own borrowings and payments

### Custom Return Endpoint
```python
POST /api/borrowings/{id}/return/
```
- Sets `actual_return_date` to current date
- Increases book inventory by 1
- Validates borrowing is not already returned
- Returns updated borrowing with nested book details

### Payment System
- Track payments associated with borrowings
- Support for regular payments and fines
- Status tracking (PENDING/PAID)
- Type classification (PAYMENT/FINE)
- Filter by status, type, and user
- Custom actions for marking payments as paid

## Development

### Running in Development Mode
```bash
# Local
python manage.py runserver

# Docker
docker-compose up
```

### Creating Migrations
```bash
# Local
python manage.py makemigrations
python manage.py migrate

# Docker
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Accessing Django Shell
```bash
# Local
python manage.py shell

# Docker
make shell
# OR
docker-compose exec web python manage.py shell
```

## License

This project is part of a Django REST Framework bootcamp assessment.