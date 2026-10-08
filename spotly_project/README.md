# Spotly — Django Place Discovery

## Included
- Full-width responsive UI with one shared design system
- Place cards show real aggregate star ratings + review count
- Place detail: reviews, 1–5 star ratings, save and Web Share/copy-link
- Verified creator blue tick controlled from Django Admin
- Login, registration, secure password reset flow
- Google OAuth login flow (requires Google Client ID/Secret)
- SQLite development default; MySQL supported via `.env`
- Clean templates and shared CSS

## Run locally
```bash
python -m venv venv
# Windows: venv\\Scripts\\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open `http://127.0.0.1:8000/`.

## Google Login
Create an OAuth Web Application in Google Cloud and set:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- Redirect URI: `http://127.0.0.1:8000/auth/google/callback/`

## Forgot Password
By default, reset emails are printed in the terminal so it works during local development. For real email delivery, set SMTP variables in `.env`.

## Verification tick
Admin → Profiles → set **Is verified**. The blue tick then appears on the creator profile, navbar and place cards/details.
