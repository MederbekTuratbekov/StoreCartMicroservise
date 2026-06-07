# User Authentication Microservice API

> Centralized auth service issuing and invalidating JWT tokens for all
platform microservices — supporting email/password login and OAuth2
social login via Google and GitHub.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Django](https://img.shields.io/badge/Django-5.x-green)]()
[![DRF](https://img.shields.io/badge/DRF-3.x-red)]()
[![JWT](https://img.shields.io/badge/Auth-JWT-orange)]()
[![OAuth2](https://img.shields.io/badge/OAuth2-Google%20%7C%20GitHub-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

## Business Problem

Monolithic auth systems become single points of failure as platforms scale.
This service centralizes identity — registration, login, logout, token
rotation, and social login — into one independently deployable unit.
All other microservices (cart, catalog) validate tokens using a shared
`JWT_SECRET` without contacting this service on every request, eliminating
auth as a bottleneck under load.

## Demo

```bash
# Register
curl -X POST http://localhost:8001/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secret123"}'
```

Response:
```json
{
  "user": {"username": "john", "email": "john@example.com"},
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

```bash
# Login
curl -X POST http://localhost:8001/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "secret123"}'

# Logout (invalidates refresh token)
curl -X POST http://localhost:8001/logout/ \
  -H "Authorization: Bearer <access_token>" \
  -d '{"refresh": "<refresh_token>"}'
```

## Approach

1. Custom `UserProfile` extends `AbstractUser` — adds age, phone, avatar, status
2. Registration validates email + username uniqueness before save
3. Login authenticates by email (not username) — returns access + refresh tokens
4. Logout blacklists refresh token via `simplejwt.token_blacklist`
5. Token rotation enabled — each refresh issues new pair, old refresh invalidated
6. Social login via `django-allauth` (Google, GitHub) at `/accounts/`
7. Deployed via Gunicorn + Nginx + Docker Compose

## Key Challenges & Solutions

**Email-based login with Django's username-first auth**
Django's default `authenticate()` requires username → implemented custom
`CustomLoginSerializer` querying by email directly →
clean email login without patching Django internals.

**Stateless logout across microservices**
JWT is stateless — logout can't invalidate tokens by default →
`BLACKLIST_AFTER_ROTATION = True` + explicit `token.blacklist()` on logout
→ refresh tokens cryptographically invalidated server-side.

**Social login alongside custom JWT flow**
`django-allauth` issues session auth; other services expect JWT →
allauth handles OAuth2 handshake; JWT issued post-authentication →
unified token format across all login methods.

## Tech Stack

| Category    | Tools                                          |
|-------------|------------------------------------------------|
| Language    | Python 3.11                                    |
| Framework   | Django 5.x, Django REST Framework             |
| Auth        | SimpleJWT, django-allauth (Google, GitHub)     |
| Phone       | django-phonenumber-field                       |
| Database    | PostgreSQL 17                                  |
| Docs        | drf-yasg (Swagger UI at `/docs/`)              |
| Deploy      | Gunicorn, Nginx, Docker Compose                |

## How to Run

```bash
git clone <repo-url> && cd StoreMicroserviseJWT
cp .env.example .env  # set SECRET_KEY, JWT_SECRET
```

```bash
docker-compose up --build
```

```bash
# Swagger UI
http://localhost:8001/docs/

# Social login
http://localhost:8001/accounts/google/login/
http://localhost:8001/accounts/github/login/
```

## Business Impact

- ↑ Single auth service — one security audit covers entire platform identity layer
- ↓ Zero auth overhead on catalog/cart services — JWT validated locally, no RPC
- ↑ Token blacklisting prevents refresh token reuse after logout
- ↑ Social login (Google + GitHub) reduces registration friction (estimated ↑15–25% conversion)
- ↓ Independent deployability — auth updates don't restart catalog or cart

[//]: # (## Author)

[//]: # ([Name] — [LinkedIn] | [GitHub])