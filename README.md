## Messenger-with-web-socket

A real-time messenger built with **Django**, **Django Channels (WebSocket)** and a custom HTML/CSS/JavaScript frontend.

### Requirements

- **Python** 3.11+ (recommended)
- **pip** / **virtualenv** (or another environment manager)

All Python dependencies are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

Main libraries:

- `Django`
- `channels` + `daphne`
- `django-jalali-date` and related Jalali / datetime utilities

### Project structure (high level)

- `manage.py` – Django management entry point  
- `messenger/` – Django project (settings, ASGI/Channels config)  
- `account/`, `main/`, `chat/` – main apps (authentication, main UI, chat logic)  
- `templates/` – HTML templates (main chat UI, login, group chat, etc.)  
- `static/assets/` – CSS, JS, fonts, and images

WebSocket routing is configured in `messenger/asgi.py` using `ProtocolTypeRouter` with `chat.routing.websocket_urlpatterns`.

### Initial setup

```bash
git clone <this-repo-url>
cd Messenger-with-web-socket

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
python manage.py createsuperuser  # optional, for admin access
```

### Running the development server (ASGI)

For local development you can use Django’s `runserver`, which will pick up the ASGI application:

```bash
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

If you prefer running via Daphne explicitly:

```bash
daphne messenger.asgi:application
```

### Static files & assets

- Static root: `static/`
- Frontend assets: `static/assets/...`

To avoid 404s for images, ensure the following directories and images exist (create/copy from the original template if needed):

- `static/assets/images/logo/` – `logo.png`, `logo_big.png`
- `static/assets/images/favicon/` – `favicon.png`
- `static/assets/images/contact/` – `1.jpg`, `2.jpg`, `3.jpg`
- `static/assets/images/avtar/` – `teq.jpg`, `girls.jpg`, `family.jpg`
- `static/assets/images/wallpaper/` – `1.jpg`–`5.jpg` (if you enable chat wallpapers)
- `static/assets/images/login_signup/` – images used on the login pages

### Key features

- One-to-one and group chats
- Real-time messaging over WebSockets
- Persian/Jalali date and time display
- Responsive RTL (right-to-left) UI

### Running tests (if/when added)

```bash
python manage.py test
```

### Notes

- This project is configured with `DEBUG = True` for local development.  
- Before deploying, make sure to:
  - Set `DEBUG = False`
  - Configure `ALLOWED_HOSTS`
  - Use a production-ready ASGI server (e.g. Daphne, Uvicorn) behind a reverse proxy

