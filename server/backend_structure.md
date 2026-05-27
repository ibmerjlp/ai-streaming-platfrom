## 1. High-Level Architecture (Phase 1)

### Tech stack
- FastAPI – API framework 
- SQLAlchemy (Async) – ORM 
- Neon - PostgreSQL Database 
- JWT – Auth 
- Pydantic – Request/response schemas 
- Alembic – Migrations 
- Passlib + bcrypt – Password hashing 

### API style
- RESTful 
- Token-based authentication 
- Stateless backend 


## 2. Industry-Standard Project Structure

This structure is commonly used in production FastAPI services.

```
app/
├── main.py
├── api/
│   ├── deps.py
│   ├── v1/
│   │   ├── api.py
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── watchlist.py
│   │   │   └── history.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── settings.py
│
├── models/
│   ├── user.py
│   ├── watchlist.py
│   └── history.py
│
├── schemas/
│   ├── user.py
│   ├── auth.py
│   ├── watchlist.py
│   └── history.py
│
├── services/
│   ├── auth_service.py
│   ├── watchlist_service.py
│   └── history_service.py
│
├── db/
│   ├── base.py
│   ├── session.py
│   └── init_db.py
│
├── crud/
│   ├── user.py
│   ├── watchlist.py
│   └── history.py
│
├── migrations/        # Alembic
│
└── tests/
    ├── test_auth.py
    ├── test_watchlist.py
    └── test_history.py
```

### Why this structure is "industry standard"
- **API layer** → handles HTTP only 
- **Services layer** → business logic 
- **CRUD layer** → database access 
- **Schemas** → request/response validation 
- **Models** → database tables 
- **Core** → configuration & security

This keeps code **testable**, **readable**, and **scalable**.


## 3. Phase 1 Feature Breakdown

### A. User Authentication (JWT)

#### Endpoints
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
GET    /api/v1/auth/me
```

#### Core responsibilities
- Register user 
- Hash passwords 
- Issue JWT access token 
- Protect routes with auth dependency

### B. Watchlist APIs

#### Endpoints
```
POST   /api/v1/watchlist
GET    /api/v1/watchlist
DELETE /api/v1/watchlist/{movie_id}
```

#### Responsibilities
- Add movie to watchlist 
- Remove movie 
- List user’s watchlist

### C. Watch History APIs

#### Endpoints
```
POST   /api/v1/history
GET    /api/v1/history
PATCH  /api/v1/history/{movie_id}
```

#### Responsibilities
- Track what user watched 
- Store progress (timestamp / completed) 
- Retrieve watch history

## 4. Authentication Flow (JWT)

### Login Flow (Industry Standard)

1. User sends email + password 
2. Verify password hash 
3. Create JWT:

   ```json
   {
     "sub": "user_id",
     "exp": 1710000000
   }
   ```

4. Return token 
5. Client sends:

   ```
   Authorization: Bearer <token>
   ```

### Security Files
```
core/security.py
```

```python
from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)
```

## 5. Database Models (Simplified)

### User

```python
class User(Base):
    id
    email
    hashed_password
    created_at
```

### Watchlist

```python
class Watchlist(Base):
    id
    user_id
    movie_id
    created_at
```

### Watch History

```python
class WatchHistory(Base):
    id
    user_id
    movie_id
    progress_seconds
    completed
    updated_at
```

## 6. API Layer Example (Watchlist)

```
api/v1/endpoints/watchlist.py
```

```python
@router.post("/")
def add_to_watchlist(
    movie: WatchlistCreate,
    current_user: User = Depends(get_current_user)
):
    return watchlist_service.add(current_user.id, movie.movie_id)
```

### Notice

- API does not touch DB directly 
- All logic lives in services/


## 7. CRUD Layer Example

```crud/watchlist.py```

```python
def create(db, user_id, movie_id):
    item = Watchlist(user_id=user_id, movie_id=movie_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
```


## 8. Best Practices (Very Important)

### Version Your API

```
/api/v1/...
```

### Never Return DB Models Directly

Always use **Pydantic schemas**

### Dependency Injection

Use `Depends()` for:

- DB session 
- Current user 
- Permissions 

### Environment Variables

Never hardcode secrets:

```
DATABASE_URL=
JWT_SECRET=
JWT_EXPIRE_MINUTES=
```

### Write Tests Early

Focus on:

- Auth flow 
- Permission checks 
- Data isolation per user


## 9. What Phase 2 Could Look Like (Future)

- Movie catalog service 
- Search & filters 
- Recommendation engine 
- Continue Watching row 
- Caching with Redis 
- Rate limiting 
- Role-based access
