# BlogAPI

A production-ready **FastAPI blogging platform** with user authentication, posts, comments, and likes. Demonstrates core backend skills including REST API design, database relationships, ORM optimization, pagination, rate limiting, nested JSON responses, and testing.

## Features

* **User Management** - Registration, login, secure JWT authentication with bcrypt
* **Blog Posts** - Create, read, update, delete posts with ownership verification
* **Comments** - Add/delete comments on posts with authorization
* **Likes** - Like/unlike posts with unique constraint (no duplicate likes)
* **Security** - JWT tokens, password hashing, SQL injection prevention, environment variables
* **Rate Limiting** - Protect API endpoints from excessive requests using SlowAPI
* **Pagination** - Paginated post responses to efficiently handle large datasets
* **Advanced Features** - Nested JSON responses, relationship optimization, database indexing

## Tech Stack

FastAPI • PostgreSQL • SQLAlchemy • JWT • bcrypt • Pydantic • pytest • SlowAPI • Neon (Deployment)

## Project Structure

```text
BlogAPI/
├── app/
│   ├── main.py           # FastAPI app
│   ├── database.py       # DB config
│   ├── models.py         # SQLAlchemy models with relationships
│   ├── schemas.py        # Pydantic response models
│   └── routers/          # auth, posts, comments, likes
├── tests/                # Unit tests
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/abenezer-gizaw/BlogAPI.git

cd BlogAPI

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

### 2. Create `.env`

```env
DATABASE_URL=postgresql://user:password@localhost/blogapi
SECRET_KEY=your-secret-key-here
```

### 3. Run

```bash
uvicorn app.main:app --reload
```

**API Docs:** http://localhost:8000/docs

## Main API Endpoints

| Endpoint              | Method | Auth | Description                          |
| --------------------- | ------ | ---- | ------------------------------------ |
| `/auth/register`      | POST   | No   | Register new user                    |
| `/auth/login`         | POST   | No   | Login & get token                    |
| `/posts`              | GET    | No   | Get paginated posts with nested data |
| `/posts`              | POST   | Yes  | Create post                          |
| `/posts/{id}`         | GET    | Yes  | Get post with comments & likes       |
| `/posts/{id}`         | PUT    | Yes  | Update post                          |
| `/posts/{id}`         | DELETE | Yes  | Delete post                          |
| `/comments/{post_id}` | POST   | Yes  | Add comment                          |
| `/comments/{id}`      | DELETE | Yes  | Delete comment                       |
| `/likes/{post_id}`    | POST   | Yes  | Like post                            |
| `/likes/{post_id}`    | DELETE | Yes  | Unlike post                          |

## Pagination

The `GET /posts` endpoint supports pagination to avoid returning an unnecessarily large dataset in a single request.

Example:

```text
GET /posts?page=1&limit=10
```

* `page` - Page number
* `limit` - Number of posts returned per page
* Helps improve response size and API performance as the number of posts grows
* Allows clients to efficiently navigate large collections

Example response:

```json
{
  "items": [
    {
      "id": 1,
      "title": "My First Blog Post",
      "content": "This is amazing!"
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

## Rate Limiting

The API uses **SlowAPI** to limit the number of requests clients can make to protected endpoints.

Rate limiting helps protect the API from excessive requests and reduces the risk of endpoint abuse.

Example:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

Endpoints can define request limits using SlowAPI decorators:

```python
@limiter.limit("10 per minute")
```

When a client exceeds the configured request limit, the API returns an HTTP `429 Too Many Requests` response.

## Database Schema & Relationships

### One-to-Many Relationships

**User → Posts (One User has Many Posts)**

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)

    owner = relationship("User", back_populates="posts")
```

* One user can create many posts
* Cascade delete: deleting a user deletes all their posts
* Back-population: access `user.posts` or `post.owner`

**Post → Comments (One Post has Many Comments)**

```python
class Post(Base):
    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete"
    )


class Comment(Base):
    __tablename__ = "comments"

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        index=True
    )

    post = relationship("Post", back_populates="comments")
```

* One post can have many comments
* Cascade delete: deleting a post deletes all comments
* Back-population allows nested data access

### Many-to-Many Relationship

**User ↔ Post (Through Likes)**

```python
class Like(Base):
    __tablename__ = "likes"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        index=True
    )
```

* Many users can like many posts
* Composite primary key ensures no duplicate likes
* Indexed foreign keys for fast queries
* `ON DELETE CASCADE` ensures referential integrity

### Database Indexing

Indexes created for performance optimization:

* `User.id` - Primary key index
* `Post.id` - Primary key index
* `Post.owner_id` - Foreign key index
* `Comment.post_id` - Foreign key index
* `Like.user_id` - Foreign key index
* `Like.post_id` - Foreign key index

## Nested JSON Response Examples

### Get All Posts

```text
GET /posts?page=1&limit=10
```

Example response:

```json
{
  "items": [
    {
      "id": 1,
      "title": "My First Blog Post",
      "content": "This is amazing!",
      "owner": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
      },
      "comments": [
        {
          "id": 1,
          "content": "Great post!",
          "user": {
            "id": 2,
            "username": "janedoe"
          }
        }
      ],
      "likes": 5
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

### Get Single Post

```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is amazing!",
  "owner": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "comments": [
    {
      "id": 1,
      "content": "Great post!",
      "user": {
        "id": 2,
        "username": "janedoe",
        "email": "jane@example.com"
      }
    },
    {
      "id": 2,
      "content": "Love it!",
      "user": {
        "id": 3,
        "username": "bobsmith"
      }
    }
  ],
  "likes": 5
}
```

## Pydantic Response Models

### Schemas (Response Models)

```python
# schemas.py

class new_user(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class new_post(BaseModel):
    title: str
    content: str


class CommentCreate(BaseModel):
    content: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = {
        "from_attributes": True
    }


class CommentUser(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True
    }


class CommentResponse(BaseModel):
    id: int
    content: str
    user: CommentUser

    class Config:
        from_attributes = True


class LikeRequest(BaseModel):
    post_id: int


class PostResponse(BaseModel):
    id: int
    title: str
    author: str
    comments: list[CommentResponse]
    likes_count: int

    model_config = {
        "from_attributes": True
    }
```

### Benefits of Pydantic Response Models

* Type validation - ensures data types are correct
* Serialization - converts SQLAlchemy models to JSON
* Nested responses - deeply nested JSON structures
* Documentation - FastAPI auto-generates API docs
* Field exclusion - hide sensitive fields
* Config options - control serialization behavior

## Testing

```bash
pytest                          # Run all tests

pytest --cov=app tests/         # With coverage report

pytest tests/test_auth.py -v    # Specific test
```

The project includes tests for authentication and API functionality.

## Security

* Passwords hashed with bcrypt
* JWT token authentication
* Rate limiting with SlowAPI
* SQL injection prevention through SQLAlchemy ORM
* Authorization checks (users modify only their own posts)
* Foreign key constraints & cascading
* Environment variables for sensitive data
* Unique constraints preventing duplicate likes

## Key Dependencies

```text
fastapi==0.136.3
sqlalchemy==2.0.50
psycopg2-binary==2.9.12
python-jose==3.5.0
bcrypt==5.0.0
pydantic==2.13.4
pytest==9.0.3
python-dotenv==1.2.2
slowapi
```

## What I Learned

* One-to-many database relationships
* Many-to-many relationships using composite keys
* SQLAlchemy `relationship()` & `back_populates`
* Cascade delete for data integrity
* Database indexing for performance
* Pagination for API scalability
* Rate limiting and API abuse prevention
* Nested JSON response design
* Pydantic response models & validation
* RESTful API best practices
* JWT authentication flow
* Unit testing with pytest

## Deployment

* PostgreSQL hosted on **Neon**
* Set `DATABASE_URL` in production environment
* Tables created automatically on startup
* Indexes optimize query performance
* Pagination helps control response size for larger datasets
* Rate limiting helps protect API endpoints from excessive requests

## Live Demo

* **API Documentation (Swagger):** https://blogapi-production-7258.up.railway.app/docs

## Author

**Abenezer Gizaw** - [@abenezer-gizaw](https://github.com/abenezer-gizaw)
