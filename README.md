# HealthyMeal Flask Project

## Tech Stack
- Python 3.x
- Flask
- SQLite (with SQLAlchemy)
- Flask-WTF, Flask-Login, Flask-Mail
- Flask-Migrate
- requests (for AI API)
- Bootstrap (for simple UI)

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On Mac/Linux
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
4. Run the app:
   ```bash
   flask run
   ```

## Notes
- Configure environment variables (e.g., `SECRET_KEY`) as needed.
- For email reset, Flask-Mail is set to use localhost:8025. Use a real SMTP server in production.
