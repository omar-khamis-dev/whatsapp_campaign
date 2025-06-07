import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / 'config'
SETTINGS_DIR = CONFIG_DIR / 'settings'
OLD_SETTINGS = CONFIG_DIR / 'settings.py'
ENV_FILE = BASE_DIR / '.env'

def ensure_init(path):
    path.mkdir(parents=True, exist_ok=True)
    (path / '__init__.py').touch(exist_ok=True)

def create_env_file():
    if not ENV_FILE.exists():
        print("[+] Creating .env file...")
        ENV_FILE.write_text(
            "DEBUG=True\n"
            "SECRET_KEY=django-insecure-1234567890\n"
            "ALLOWED_HOSTS=127.0.0.1,localhost\n"
            "LANGUAGE_CODE=ar\n"
            "TIME_ZONE=Asia/Aden\n"
        )

def create_settings_files():
    print("[+] Creating settings directory structure...")
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    ensure_init(SETTINGS_DIR)

    base_file = SETTINGS_DIR / 'base.py'
    dev_file = SETTINGS_DIR / 'dev.py'
    prod_file = SETTINGS_DIR / 'prod.py'

    base_content = f"""
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.campaign',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
TIME_ZONE = config('TIME_ZONE', default='UTC')
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""

    dev_content = "from .base import *\n"
    prod_content = "from .base import *\nDEBUG = False\n"

    base_file.write_text(base_content.strip(), encoding='utf-8')
    dev_file.write_text(dev_content, encoding='utf-8')
    prod_file.write_text(prod_content, encoding='utf-8')

    if OLD_SETTINGS.exists():
        OLD_SETTINGS.unlink()

def update_entrypoint(file_path: Path):
    if file_path.exists():
        content = file_path.read_text(encoding='utf-8')
        content = content.replace(
            "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')",
            "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')"
        )
        file_path.write_text(content, encoding='utf-8')

def update_apps_py():
    apps_path = BASE_DIR / 'apps' / 'campaign' / 'apps.py'
    if apps_path.exists():
        content = apps_path.read_text(encoding='utf-8')
        if "name = 'apps.campaign'" not in content:
            content = content.replace("name = 'campaign'", "name = 'apps.campaign'")
            apps_path.write_text(content, encoding='utf-8')

def ensure_all_inits():
    ensure_init(BASE_DIR / 'apps')
    ensure_init(BASE_DIR / 'apps' / 'campaign')
    ensure_init(CONFIG_DIR)

def main():
    print("[*] Restructuring Django project with .env support...")
    create_env_file()
    create_settings_files()
    update_entrypoint(BASE_DIR / 'manage.py')
    update_entrypoint(CONFIG_DIR / 'wsgi.py')
    update_entrypoint(CONFIG_DIR / 'asgi.py')
    update_apps_py()
    ensure_all_inits()
    print("[✔] Project structure restructured successfully with .env support!")

if __name__ == "__main__":
    main()
