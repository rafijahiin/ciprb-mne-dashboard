# ciprb-mne-dashboard
## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ciprb-mne-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Copy the example environment file and fill in your actual secrets:
   ```bash
   cp .env.example .env
   ```
   **Required Variables:**
   - `DATABASE_URL`: Connection string for PostgreSQL (e.g., Supabase).
   - `GEMINI_API_KEY`: Google Gemini API key for the AI Newsletter generation.
   - `KOBO_WEBHOOK_SECRET`: Secure token for authenticating KoboToolbox webhooks.

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
