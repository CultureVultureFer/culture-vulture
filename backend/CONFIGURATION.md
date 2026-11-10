# Culture Vulture Backend

## Running the Project

### With Docker Compose (PostgreSQL + Backend)

From the repository root, run:
```bash
docker compose up -d
```
This starts both PostgreSQL (`psql`) and the Django backend (`backend` on `http://localhost:8000`), runs migrations, and creates a default superuser automatically.

### Running Django Locally with `uv`

If you want to run only PostgreSQL in Docker and run Django on your host:
```bash
docker compose up -d psql
```

Make sure your `backend/.env` contains the database connection variables (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST=localhost`, `POSTGRES_PORT=5432`), then from `/backend` run:
```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser   # admin for /admin, gets the ADMIN role
uv run python manage.py runserver
```

### Tests & Type Checking

Run tests from `/backend` (PostgreSQL must be running):
```bash
uv run python manage.py test
```

Run type checking:
```bash
uv run basedpyright
```

## Authentication (F-001)

Regular users register and log in **with Google** (OpenID Connect). There are no app passwords for OIDC users, so no password reset or email verification is needed: Google has already verified the email. Login state is kept in a Django session cookie (`sessionid`, HttpOnly); the frontend never stores tokens.

- **User:** "Sign in with Google" -> the first login creates the account (role `USER`) with a deterministic UUID (`uuid5(NAMESPACE_OID, sub)`).
- **Organizer:** registers **once** with an organization name, then signs in with Google (see below). Every later login is the normal "Sign in with Google", exactly like a user.
- **Admin:** `createsuperuser` (email + password, used for `/admin`, gets role `ADMIN`).

### Organizer registration

One URL, two steps:

1. `POST /api/auth/organization/register/` with `{"name": "Klub Močvara"}` (`fetch`). The name is validated and remembered in the session.
   - `200 {"redirect": "/api/auth/organization/register/"}`
   - `400 {"errors": {"name": [...]}}` (missing, longer than 150 characters, or not allowed characters), `400 {"errors": {"__all__": ["Invalid JSON."]}}`, `400 {"errors": {"__all__": ["You already have an account."]}}` (already logged in)
2. The frontend navigates to `redirect` (`window.location.assign`), i.e. `GET /api/auth/organization/register/`, which sends the browser to Google. After Google the normal callback:
   - **new Google account:** if an organization with that name exists (case-insensitive) the organizer **joins** it, otherwise a new organization is created. The account gets role `ORGANIZER`, is logged in and redirected to `/hello`.
   - **existing account:** just logs in, like a normal login (the name is ignored, the role does not change).

One organization can have many organizers; a user belongs to at most one organization. The pending name is valid for one Google attempt only, and a normal login (`/api/auth/google/login/`) clears it, so an abandoned registration never turns a later login into a registration.

```js
await fetch("/api/auth/csrf/");
const csrftoken = document.cookie.match(/csrftoken=([^;]+)/)[1];
const res = await fetch("/api/auth/organization/register/", {
  method: "POST",
  headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
  body: JSON.stringify({ name }),
});
if (res.ok) window.location.assign((await res.json()).redirect);
else showErrors((await res.json()).errors);   // e.g. errors.name
```

> **Existing local databases must be reset** if migrating from an older schema (`AUTH_USER_MODEL = 'accounts.User'` with UUID primary key):
> ```bash
> docker compose down -v
> docker compose up -d
> ```

### API

All POST requests need the `X-CSRFToken` header (obtain the `csrftoken` cookie from `GET /api/auth/csrf/`).

| Method | URL | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/api/auth/csrf/` | – | 204, sets `csrftoken` cookie | – |
| GET | `/api/auth/me/` | – | 200 user | 401 |
| GET | `/api/auth/google/login/` | – | redirect to Google | – |
| GET | `/api/auth/google/callback/` | (called by Google) | redirect to `/hello` | redirect to `/login?auth_error=<code>` |
| POST | `/api/auth/logout/` | – | 204 | – |
| POST | `/api/auth/organization/register/` | `{"name": "..."}` | 200 `{"redirect": ...}` | 400 |
| GET | `/api/auth/organization/register/` | – | redirect to Google | redirect to `/login?auth_error=organization_not_registered` (no name posted first) |

`auth_error` codes on `/login`:

| Code | Meaning |
|---|---|
| `cancelled` | User cancelled on Google |
| `oidc_error` | Google response invalid (e.g. tampered `state`) |
| `invalid_token` | Google token has no `sub` |
| `user_already_logged_in` | Someone is already logged in in this browser |
| `account_disabled` | Account is deactivated (`is_active = False`) |
| `email_not_verified` | Google email is not verified |
| `email_exists` | Another account already uses this email |
| `organization_not_registered` | Organizer registration step 2 without step 1 |

User object:
```json
{"id": "550e8400-e29b-41d4-a716-446655440000", "username": "Marko Marić", "email": "marko@gmail.com", "role": "USER"}
```

Error object (401), messages per field, `__all__` for general ones:
```json
{"errors": {"__all__": ["Not logged in."]}}
```

### Google setup (once per developer)

1. Ask the team for the Google OAuth **Client ID** and **Client secret**
   (one Google Cloud project for the whole team).
2. Copy `backend/.env.example` to `backend/.env` (`copy .env.example .env` on Windows / `cp .env.example .env` on Linux/macOS) and fill them in.
3. In Google Cloud Console the client must have the redirect URI
   `http://localhost:5173/api/auth/google/callback/`, and your Gmail must be
   in *Audience -> Test users* while the app is in testing mode.
4. Open the app on **http://localhost:5173** (Vite proxies `/api` to Django),
   not on `:8000`, otherwise cookies won't match.

### Data model (vs. ERD 4-2)

| ERD | Code |
|---|---|
| ROLE | `accounts.Role` (`USER`, `ORGANIZER`, `ADMIN`) |
| USER | `accounts.User` (UUID `id` derived from Google `sub` via `uuid5` for OIDC users, `email` from Google, `username` = display name, `date_joined` = created_at, `organization` = FK to `Organization`, set only for organizers) |
| ORGANIZATION (new, not in ERD yet) | `accounts.Organization` (UUID `id`, `name` unique case-insensitive, `created_at`); many organizers per organization, deleting an organization that still has organizers is blocked (`PROTECT`) |
| OAUTH_ACCOUNTS | Removed (`accounts.User.id` is derived deterministically from the Google OIDC `sub` claim) |
| SESSIONS | Django sessions (`django_session` table), no custom model |

