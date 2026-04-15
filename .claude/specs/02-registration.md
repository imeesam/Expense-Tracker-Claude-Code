# Spec: Registration

## Overview

Implement the user registration feature that allows new users to create an account.
This feature enables users to sign up by providing their name, email, and password.
Upon successful registration, users will be redirected to the login page to sign in.
This is the second step in building the authentication system for Spendly.

## Depends on

- Step 1 (Database Setup) — requires the `users` table and `get_db()` function to exist

## Routes

- `POST /register` — handles form submission for new user registration — public

## Database changes

No database changes — the `users` table from Step 1 is sufficient.

## Templates

- **Modify:** `templates/register.html` — add a registration form with fields for:
  - Name (text input)
  - Email (email input)
  - Password (password input)
  - Submit button
  - Display flash messages for errors (e.g., email already exists, missing fields)
  - Link to login page for existing users

## Files to change

- `app.py` — add POST handler for `/register` route with form processing logic
- `templates/register.html` — add the registration form UI

## Files to create

- None

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs — use raw SQLite via `database/db.py`
- Parameterized queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use `flash()` for success/error messages — display them in the template
- Redirect to login page after successful registration
- Validate required fields: name, email, password must not be empty
- Check for duplicate email before inserting — show error if email exists
- All templates extend `base.html`
- Use `url_for()` for all internal links — never hardcode URLs

## Definition of done

- [ ] Registration form displays with name, email, password fields
- [ ] Submitting empty fields shows an error message
- [ ] Submitting an existing email shows an error message
- [ ] Successful registration creates a new user in the database
- [ ] Password is stored as a hash, not plain text
- [ ] User is redirected to login page after successful registration
- [ ] Flash message confirms successful registration
- [ ] Link to login page is present on registration page
- [ ] App handles duplicate email gracefully with clear error
