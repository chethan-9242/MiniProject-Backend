# SwasthVedha Backend — PostgreSQL Connection Guide

Use this page as a PDF (Print to PDF) for your records.

---

## 1) .env configuration

Keep the individual password plain, but URL‑encode it only inside the connection URL.

```
# Components
DB_USER=swasthvedha
DB_PASSWORD=Chethan@12345
DB_HOST=localhost
DB_PORT=5432
DB_NAME=SwasthVedha

# Final URL (password URL‑encoded: @ -> %40)
DATABASE_URL=postgresql+psycopg2://swasthvedha:Chethan%4012345@localhost:5432/SwasthVedha
```

Notes
- Only encode special characters when they appear inside `DATABASE_URL`.
- Examples to encode: `@` -> `%40`, `:` -> `%3A`, `/` -> `%2F`, `#` -> `%23`.

---

## 2) Create/verify DB and role in pgAdmin

Database
- Name: `SwasthVedha` (exact case if you created it with capitals)
- Owner: `swasthvedha`

Role (user)
- Role name: `swasthvedha`
- Login: enabled
- Password: `Chethan@12345`

Connection test in pgAdmin (Server > Register)
- Host: `localhost`
- Port: `5432`
- Maintenance DB: `postgres`
- Username: `swasthvedha`
- Password: `Chethan@12345`

---

## 3) Run the backend with env file

PowerShell (from `backend/`):
```
uvicorn main:app --reload --env-file .env
```
Then open:
```
http://localhost:8000/db/ping
```
Expected: a JSON with database status.

---

## 4) Troubleshooting

- Error: `password authentication failed for user "postgres"`
  - Cause: you are connecting as `postgres` instead of `swasthvedha`.
  - Fix: update pgAdmin connection and `DATABASE_URL` to use `swasthvedha`.

- Error: `database "SwasthVedha" does not exist`
  - Create DB in pgAdmin (Databases > Create > Database) and set owner `swasthvedha`.

- Error: `FATAL: role "swasthvedha" does not exist`
  - Create role: pgAdmin > Login/Group Roles > Create > Login/Group Role.

- Special characters in password
  - Keep plain in `DB_PASSWORD`; URL‑encode only within `DATABASE_URL`.

---

## 5) Optional CLI checks

```
# Using psql if installed
psql -h localhost -p 5432 -U swasthvedha -d SwasthVedha
```
(Enter `Chethan@12345` when prompted.)

---

Revision: 2025‑10‑18
