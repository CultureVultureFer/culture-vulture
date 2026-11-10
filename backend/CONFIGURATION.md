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
- **Organizator:** registrira se **jednom** s nazivom organizacije, a zatim se prijavi preko Googlea (vidi niže). Svaka kasnija prijava je obična "Sign in with Google", potpuno ista kao kod korisnika.
- **Admin:** `createsuperuser` (email + password, used for `/admin`, gets role `ADMIN`).

### Registracija organizatora

Jedna adresa, dva koraka:

1. `POST /api/auth/organization/register/` s `{"name": "Klub Močvara"}` (`fetch`). Naziv se provjeri i zapamti u sesiji.
   - `200 {"redirect": "/api/auth/organization/register/"}`
   - `400 {"errors": {"name": [...]}}` (naziv nedostaje, dulji je od 150 znakova ili sadrži nedopuštene znakove), `400 {"errors": {"__all__": ["Invalid JSON."]}}`, `400 {"errors": {"__all__": ["You already have an account."]}}` (korisnik je već prijavljen)
2. Frontend otvori adresu iz `redirect` (`window.location.assign`), tj. `GET /api/auth/organization/register/`, koja preglednik pošalje na Google. Nakon Googlea uobičajeni callback:
   - **novi Google račun:** ako organizacija s tim nazivom postoji (bez obzira na velika i mala slova), organizator joj se **pridruži**, a inače se kreira nova organizacija. Račun dobiva ulogu `ORGANIZER`, prijavljuje se i preusmjerava na `/hello`.
   - **postojeći račun:** samo se prijavi, kao kod obične prijave (naziv se ignorira, uloga se ne mijenja).

Jedna organizacija može imati više organizatora; korisnik pripada najviše jednoj organizaciji. Zapamćeni naziv vrijedi samo za jedan pokušaj prijave na Googleu, a obična prijava (`/api/auth/google/login/`) ga briše, pa odustala registracija nikad ne pretvori kasniju prijavu u registraciju.

```js
await fetch("/api/auth/csrf/");
const csrftoken = document.cookie.match(/csrftoken=([^;]+)/)[1];
const res = await fetch("/api/auth/organization/register/", {
  method: "POST",
  headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
  body: JSON.stringify({ name }),
});
if (res.ok) window.location.assign((await res.json()).redirect);
else showErrors((await res.json()).errors);   // npr. errors.name
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
| GET | `/api/auth/organization/register/` | – | preusmjeravanje na Google | preusmjeravanje na `/login?auth_error=organization_not_registered` (naziv prije toga nije poslan) |

Kodovi `auth_error` na `/login`:

| Kod | Značenje |
|---|---|
| `cancelled` | Korisnik je odustao na Googleu |
| `oidc_error` | Neispravan odgovor Googlea (npr. podmetnut `state`) |
| `invalid_token` | Googleov token nema `sub` |
| `user_already_logged_in` | U ovom pregledniku je netko već prijavljen |
| `account_disabled` | Račun je deaktiviran (`is_active = False`) |
| `email_not_verified` | Google e-mail nije potvrđen |
| `email_exists` | Drugi račun već koristi ovaj e-mail |
| `organization_not_registered` | 2. korak registracije organizatora bez 1. koraka |

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
| USER | `accounts.User` (UUID `id` derived from Google `sub` via `uuid5` for OIDC users, `email` from Google, `username` = display name, `date_joined` = created_at, `organization` = FK na `Organization`, postavljen samo za organizatore) |
| ORGANIZATION (novo, još nije u ERD-u) | `accounts.Organization` (UUID `id`, `name` jedinstven bez obzira na velika i mala slova, `created_at`); više organizatora po organizaciji, brisanje organizacije koja još ima organizatore je blokirano (`PROTECT`) |
| OAUTH_ACCOUNTS | Removed (`accounts.User.id` is derived deterministically from the Google OIDC `sub` claim) |
| SESSIONS | Django sessions (`django_session` table), no custom model |

