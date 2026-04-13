# CampaignOps API

A production-oriented **FastAPI backend** for authenticated content operations, built with **PostgreSQL, SQLAlchemy, Alembic, JWT auth, Nginx, and Gunicorn**.

This project demonstrates how to design and deploy a backend API with:
- secure user authentication
- role-aware ownership of content
- vote-based engagement tracking
- migration-based schema management
- deployment-ready Linux server configuration

Rather than relying on `create_all()` to generate tables at runtime, the project uses **Alembic migrations** for safer schema evolution and a more realistic production workflow.

---

## Core Features

### Authentication & Security
- User registration with hashed passwords using **bcrypt / Passlib**
- Login with **OAuth2PasswordRequestForm**
- JWT access token creation and validation using **python-jose**
- Protected routes using FastAPI dependencies

### Content Management
- Create, read, update, and delete posts
- Associate each post with its owner
- Restrict certain operations to the authenticated user
- Search posts by title
- Pagination support with `limit` and `skip`

### Engagement Tracking
- Vote/unvote on posts
- Prevent duplicate votes from the same user
- Aggregate vote counts using SQLAlchemy joins and `COUNT()`
- Return enriched post responses with vote totals

### Database & Backend Architecture
- PostgreSQL-backed relational data model
- SQLAlchemy ORM for models and queries
- Pydantic schemas for validation and serialization
- Alembic migration workflow for schema versioning
- Centralized environment-based configuration with `pydantic-settings`

### Deployment Readiness
- Nginx reverse proxy configuration included
- Gunicorn systemd service file included
- App structured for deployment to a Linux VM/server

---

## Tech Stack

**Backend**
- FastAPI
- Python
- SQLAlchemy
- Pydantic v2

**Database**
- PostgreSQL
- Alembic

**Authentication**
- OAuth2 password flow
- JWT (`python-jose`)
- Passlib / bcrypt

**Deployment**
- Gunicorn
- Uvicorn worker
- Nginx
- Linux systemd service

---

## Architecture Overview

```text
Client / Postman
      |
      v
   Nginx (reverse proxy)
      |
      v
Gunicorn + Uvicorn Workers
      |
      v
 FastAPI Application
      |
      +--> Auth Router (/login)
      +--> User Router (/users)
      +--> Post Router (/posts)
      +--> Vote Router (/vote)
      |
      v
 SQLAlchemy ORM
      |
      v
 PostgreSQL
```

---

## Data Model

### Users
Stores registered users with:
- `id`
- `email`
- `password` (hashed)
- `created_at`

### Posts
Stores content created by authenticated users:
- `id`
- `title`
- `content`
- `published`
- `created_at`
- `owner_id` → foreign key to `users.id`

### Votes
Tracks which user voted on which post:
- `user_id`
- `post_id`

This uses a **composite primary key** to prevent duplicate user-post vote combinations.

---

## API Endpoints

### Auth
- `POST /login` → authenticate user and receive JWT access token

### Users
- `POST /users` → create a new user
- `GET /users/{id}` → fetch a user by ID

### Posts
- `GET /posts` → get posts with vote counts, pagination, and search
- `POST /posts` → create a post
- `GET /posts/{id}` → get one post with vote count
- `PUT /posts/{id}` → update a post
- `DELETE /posts/{id}` → delete a post

### Votes
- `POST /vote` → add or remove a vote from a post

---

## Example Request Flow

### 1. Create a user
```http
POST /users
```

```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

### 2. Log in
```http
POST /login
```
Form data:
```text
username=user@example.com
password=strongpassword123
```

### 3. Use the returned token
```http
Authorization: Bearer <access_token>
```

### 4. Create a post
```http
POST /posts
```

```json
{
  "title": "Launching a new campaign",
  "content": "Campaign planning and execution details.",
  "published": true
}
```

### 5. Vote on a post
```http
POST /vote
```

```json
{
  "post_id": 1,
  "dir": 1
}
```

---

## Project Structure

```bash
campaignops-api/
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── user.py
│   │   └── vote.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── schemas.py
│   └── utils.py
├── alembic/
│   ├── env.py
│   └── versions/
├── nginx
├── gunicorn.service
├── alembic.ini
└── requirements.txt
```

### Folder/File Purpose
- `app/main.py` → FastAPI app entry point and router registration
- `app/models.py` → SQLAlchemy models for users, posts, and votes
- `app/schemas.py` → request/response models
- `app/oauth2.py` → JWT creation, verification, and current-user dependency
- `app/utils.py` → password hashing and verification helpers
- `app/database.py` → database connection and session dependency
- `app/routers/` → grouped route logic by feature
- `alembic/` → migration environment and version history
- `nginx` → reverse proxy config for deployment
- `gunicorn.service` → Linux service definition for production app execution

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/campaignops-api.git
cd campaignops-api
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file
Use environment variables similar to:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=yourpassword
DATABASE_NAME=campaignops
DATABASE_USERNAME=yourusername
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run migrations
```bash
alembic upgrade head
```

### 6. Start the API
```bash
uvicorn app.main:app --reload
```

The app will run at:
```text
http://127.0.0.1:8000
```

Interactive docs:
```text
http://127.0.0.1:8000/docs
```

---

### Gunicorn
A `gunicorn.service` file is included to run the FastAPI app with Uvicorn workers under systemd.

### Nginx
An Nginx config is included to:
- listen on port 80
- forward requests to the FastAPI app on port 8000
- preserve important proxy headers

This setup reflects a common Linux VM deployment pattern:

```text
Internet -> Nginx -> Gunicorn/Uvicorn -> FastAPI -> PostgreSQL
```


