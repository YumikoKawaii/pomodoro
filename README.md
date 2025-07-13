# FastAPI Backend Project with MySQL

A well-structured FastAPI backend project with MySQL database integration, SQLAlchemy ORM, and Alembic migrations.

## Project Structure

```
fastapi-backend/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   └── routers/
│       ├── __init__.py
│       ├── items.py
│       └── users.py
├── alembic/
│   ├── env.py
│   └── versions/
├── main.py
├── create_db.py
├── alembic.ini
├── requirements.txt
├── .env
└── README.md
```

## Features

- **FastAPI** with automatic OpenAPI documentation
- **MySQL** database integration with SQLAlchemy ORM
- **Alembic** for database migrations
- **Pydantic** models for data validation
- **Password hashing** with bcrypt
- **CORS** middleware configured
- **Environment-based configuration**
- **Modular CRUD operations**
- **Database connection pooling**
- **Proper error handling**

## Prerequisites

1. **MySQL Server** installed and running
2. **Python 3.8+**
3. **MySQL database** created for the project

## Installation

1. **Create MySQL Database**:
   ```sql
   CREATE DATABASE fastapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'fastapi_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON fastapi_db.* TO 'fastapi_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **Clone or create the project structure** as shown above

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Update the `.env` file with your MySQL credentials:
   ```env
   DATABASE_URL=mysql+pymysql://fastapi_user:your_password@localhost:3306/fastapi_db
   ```

6. **Initialize the database**:
   ```bash
   # Option 1: Create tables directly
   python create_db.py
   
   # Option 2: Use Alembic migrations (recommended)
   alembic init alembic  # Only if alembic folder doesn't exist
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

## Running the Application

1. **Start the development server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the application**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Database Operations

### Using Alembic for Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1

# View migration history
alembic history
```

### Direct Database Operations

```bash
# Create all tables
python create_db.py

# Access MySQL directly
mysql -u fastapi_user -p fastapi_db
```

## API Endpoints

### Root Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check

### Items
- `GET /api/v1/items/` - Get all items (with pagination and filtering)
- `GET /api/v1/items/{item_id}` - Get specific item
- `POST /api/v1/items/` - Create new item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item
- `GET /api/v1/items/stats/count` - Get items count

### Users
- `GET /api/v1/users/` - Get all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get specific user
- `POST /api/v1/users/` - Create new user (with password hashing)
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

## Example Usage

### Create a user:
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "securepassword123",
    "is_active": true
  }'
```

### Create an item:
```bash
curl -X POST "http://localhost:8000/api/v1/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Keyboard",
    "description": "Mechanical keyboard",
    "price": 99.99,
    "is_active": true
  }'
```

### Get items with filtering:
```bash
curl "http://localhost:8000/api/v1/items/?skip=0&limit=10&is_active=true"
```

## Configuration

The application uses environment variables for configuration:

- `DATABASE_URL`: MySQL connection string
- `PROJECT_NAME`: Application name
- `VERSION`: Application version
- `ENVIRONMENT`: Environment (development/production)
- `DEBUG`: Enable debug mode
- `SECRET_KEY`: Secret key for security

## Database Schema

### Items Table
- `id`: Primary key
- `name`: Item name (max 100 chars)
- `description`: Item description (text)
- `price`: Item price (float)
- `is_active`: Active status (boolean)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Users Table
- `id`: Primary key
- `email`: User email (unique)
- `username`: Username (unique, max 50 chars)
- `full_name`: Full name (max 100 chars)
- `hashed_password`: Bcrypt hashed password
- `is_active`: Active status (boolean)
- `created_at`: Creation timestamp

## Security Features

- **Password hashing** using bcrypt
- **Email validation** using Pydantic
- **Unique constraints** on email and username
- **SQL injection protection** via SQLAlchemy ORM
- **Input validation** via Pydantic models

## Development Notes

- All database operations use SQLAlchemy ORM for security
- Password hashing is handled automatically in CRUD operations
- Database sessions are properly managed with dependency injection
- Connection pooling is configured for better performance

## Next Steps

To extend this project further:

1. **Add JWT authentication**
2. **Implement user roles and permissions**
3. **Add relationship between users and items**
4. **Implement caching with Redis**
5. **Add comprehensive logging**
6. **Write unit and integration tests**
7. **Add background tasks with Celery**
8. **Containerize with Docker**
9. **Add API rate limiting**
10. **Implement full-text search**