import os
from dotenv import load_dotenv

load_dotenv()

def _env_bool(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Default to SQLite for local/dev unless DATABASE_URL is provided
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Rate limiting storage (use Redis in prod e.g., redis://localhost:6379/0)
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
    # Secure session cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    SESSION_COOKIE_SECURE = _env_bool('SESSION_COOKIE_SECURE', False)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = _env_bool('REMEMBER_COOKIE_SECURE', False)
    REMEMBER_COOKIE_SAMESITE = os.environ.get('REMEMBER_COOKIE_SAMESITE', 'Lax')
    # Uploads
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_UPLOAD_MB', '20')) * 1024 * 1024
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = _env_bool('MAIL_USE_TLS', True)
    MAIL_USE_SSL = _env_bool('MAIL_USE_SSL', False)
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME or 'no-reply@example.com')
