# Culture Vulture Backend
To start project locally run:
```
docker compose up -d
```
to start the postgresql db using docker image...

And from `/backend` run:
```
uv run python manage.py runserver
```
to start the project locally...

Before the first run (and after pulling new migrations):
```
uv run python manage.py migrate
uv run python manage.py createsuperuser   # admin for /admin, gets the ADMIN role
```

Run tests (database must be running):
```
uv run python manage.py test
```

## Authentication (F-001)

Everyone (users and organizers) registers and logs in **only with Google**
(OpenID Connect). There are no app passwords, so no password reset or email
verification is needed: Google has already verified the email. Login state is
kept in a Django session cookie (`sessionid`, HttpOnly); the frontend never
stores tokens.

- **User:** "Sign in with Google" -> the first login creates the account (role USER).
- **Organizer:** sign in with Google, then submit the organization name to
  `/api/auth/register/organizer/` -> role ORGANIZER.
- **Admin:** `createsuperuser` (email + password, used only for `/admin`).

> **Existing local databases must be reset once** because this adds a custom
> user model (`AUTH_USER_MODEL = 'accounts.User'`):
> ```
> docker compose down -v
> docker compose up -d
> uv run python manage.py migrate
> ```

### API

All POST requests need the `X-CSRFToken` header (get the cookie from
`GET /api/auth/csrf/`). `frontend/src/api/auth.js` does this for you.

| Method | URL | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/api/auth/csrf/` | – | 204, sets `csrftoken` cookie | – |
| GET | `/api/auth/me/` | – | 200 user | 401 |
| GET | `/api/auth/google/login/?next=/path` | – | redirect to Google | – |
| GET | `/api/auth/google/callback/` | (called by Google) | redirect to `next` | redirect to `/login?auth_error=<code>` |
| POST | `/api/auth/register/organizer/` | `{name}` (must be logged in) | 200 organizer | 400, 401 |
| POST | `/api/auth/logout/` | – | 204 | – |

User object:
```json
{"id": 1, "username": "Kino Europa", "email": "info@kino.hr", "role": "ORGANIZER"}
```

Error object (400/401), messages per form field, `__all__` for general ones:
```json
{"errors": {"name": ["An organization with this name already exists."]}}
```

### Google setup (once per developer)

1. Ask the team for the Google OAuth **Client ID** and **Client secret**
   (one Google Cloud project for the whole team).
2. `copy .env.example .env` (Windows) / `cp .env.example .env` and fill them in.
3. In Google Cloud Console the client must have the redirect URI
   `http://localhost:5173/api/auth/google/callback/`, and your Gmail must be
   in *Audience -> Test users* while the app is in testing mode.
4. Open the app on **http://localhost:5173** (Vite proxies `/api` to Django),
   not on :8000, otherwise cookies won't match.

### Data model (vs. ERD 4-2)

| ERD | Code |
|---|---|
| ROLE | `accounts.Role` (USER, ORGANIZER, ADMIN; created by migration `0002_seed_roles`) |
| USER | `accounts.User` (email from Google, `username` = display / organization name, `date_joined` = created_at) |
| OAUTH_ACCOUNTS | `accounts.OAuthAccount` |
| SESSIONS | Django sessions (`django_session` table), no own model |
