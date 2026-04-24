import os
import re
import secrets
from pathlib import Path


class DjangoProjectGenerator:
    BASE_PACKAGES = [
        ("Django", ">=5.2,<6.0"),
        ("djangorestframework", ">=3.17"),
        ("django-cors-headers", ">=4.9"),
        ("python-decouple", ">=3.8"),
        ("psycopg2-binary", ">=2.9"),
        ("django-phonenumber-field", ">=8.4"),
        ("Pillow", ">=11"),
        ("django-redis", ">=5.0"),
    ]

    def __init__(self, project_name: str):
        self.project_name = self._slugify(project_name)
        self.base_dir = Path.cwd() / self.project_name
        self.src_dir = self.base_dir / "src" / self.project_name

    def _slugify(self, name: str) -> str:
        name = re.sub(r"[^a-zA-Z0-9]", "-", name)
        name = re.sub(r"-+", "-", name).strip("-")
        return name.lower()

    def _generate_secret_key(self) -> str:
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)"
        return "".join(secrets.choice(chars) for _ in range(50))

    def generate(self):
        print(f"Creating Django project '{self.project_name}'...")
        self._create_directory_structure()
        self._create_manage_py()
        self._create_project_package()
        self._create_settings_module()
        self._create_users_app()
        self._create_env_example()
        self._create_requirements_txt()
        self._create_gitignore()
        print(f"\nDone! Project created at: {self.base_dir}")
        print(f"\nTo get started:")
        print(f"  cd {self.project_name}")
        print(f"  cp src/.env.example src/.env")
        print(f"  python -m venv venv")
        print(f"  source venv/bin/activate")
        print(f"  pip install -r requirements.txt")
        print(f"  python src/manage.py migrate")

    def _create_directory_structure(self):
        (self.base_dir).mkdir(parents=True)
        (self.src_dir).mkdir(parents=True)
        (self.src_dir / "users" / "migrations").mkdir(parents=True)

    def _create_manage_py(self):
        content = f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.project_name}.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''
        path = self.src_dir / "manage.py"
        path.write_text(content)
        os.chmod(path, 0o755)

    def _create_project_package(self):
        init_file = self.src_dir / self.project_name / "__init__.py"
        init_file.parent.mkdir(parents=True)
        init_file.write_text("")

        urls_content = f'''from django.contrib import admin
from django.urls import path
from {self.project_name}.views import api_root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),
]
'''
        (self.src_dir / self.project_name / "urls.py").write_text(urls_content)

        views_content = f'''from django.http import JsonResponse


def api_root(request):
    return JsonResponse({{"message": "Welcome to {self.project_name}", "status": "ok"}})
'''
        (self.src_dir / self.project_name / "views.py").write_text(views_content)

        admin_content = f'''from django.contrib import admin


# Register your models here.
'''
        (self.src_dir / self.project_name / "admin.py").write_text(admin_content)

        models_content = f'''import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
'''
        (self.src_dir / self.project_name / "models.py").write_text(models_content)

        utils_content = f'''import base64
import uuid


def get_random_id(prefix=""):
    encoded = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return prefix + encoded.rstrip(b"=").decode("ascii")
'''
        (self.src_dir / self.project_name / "utils.py").write_text(utils_content)

        wsgi_content = f'''"""
WSGI config for {self.project_name} project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.project_name}.settings.development')

application = get_wsgi_application()
'''
        (self.src_dir / self.project_name / "wsgi.py").write_text(wsgi_content)

        asgi_content = f'''"""
ASGI config for {self.project_name} project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.project_name}.settings.development')

application = get_asgi_application()
'''
        (self.src_dir / self.project_name / "asgi.py").write_text(asgi_content)

    def _create_settings_module(self):
        settings_dir = self.src_dir / self.project_name / "settings"
        settings_dir.mkdir(parents=True)

        (settings_dir / "__init__.py").write_text("")

        common_settings = f'''import os
from pathlib import Path
from corsheaders.defaults import default_headers
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")

CURRENT_ENV = None

ENV_PREPROD = "preprod"
ENV_PROD = "production"
ENV_DEV = "dev"

SECRET_KEY = config('DJANGO_SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'phonenumber_field',
    'users',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{self.project_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{self.project_name}.wsgi.application'

DATABASES = {{
    "default": {{
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }}
}}

AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

PHONENUMBER_DEFAULT_REGION = "IN"
AUTH_USER_MODEL = "users.User"

STATIC_URL = 'static/'
STATICFILES_LOCATION = "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = (*default_headers,)

CACHES = {{
    "default": {{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": {{config('REDIS_URL')}},
        "OPTIONS": {{
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }},
    }}
}}
'''
        (settings_dir / "common.py").write_text(common_settings)

        dev_settings = f'''from settings.common import *

CURRENT_ENV = ENV_DEV
'''
        (settings_dir / "development.py").write_text(dev_settings)

        preprod_settings = f'''from settings.common import *

CURRENT_ENV = ENV_PREPROD
'''
        (settings_dir / "preprod.py").write_text(preprod_settings)

        prod_settings = f'''from settings.common import *

CURRENT_ENV = ENV_PROD
DEBUG = False
'''
        (settings_dir / "production.py").write_text(prod_settings)

    def _create_users_app(self):
        users_dir = self.src_dir / "users"

        (users_dir / "__init__.py").write_text("")
        (users_dir / "apps.py").write_text(
            'from django.apps import AppConfig\n\n\nclass UsersConfig(AppConfig):\n    default_auto_field = "django.db.models.BigAutoField"\n    name = "users"\n'
        )
        (users_dir / "admin.py").write_text(
            'from django.contrib import admin\nfrom users.models import User\n\n\n@admin.register(User)\nclass UserAdmin(admin.ModelAdmin):\n    list_display = ["email", "username", "phone", "is_active", "is_staff"]\n    search_fields = ["email", "username", "phone"]\n'
        )
        (users_dir / "views.py").write_text(
            'from django.http import JsonResponse\n\n\ndef health_check(request):\n    return JsonResponse({"status": "ok"})\n'
        )
        (users_dir / "tests.py").write_text(
            'from django.test import TestCase\n\n\nclass UserModelTest(TestCase):\n    pass\n'
        )
        (users_dir / "migrations" / "__init__.py").write_text("")

        models_content = f'''from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from {self.project_name}.models import BaseModel
from {self.project_name}.utils import get_random_id


class UserManager(BaseUserManager):
    def _create_user(self, email, password, *args, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, *args, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_active", True)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, *args, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be a staff")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be a superuser")
        return self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return f"{{self.name}}({{self.email}})"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = get_random_id("U")
        super().save(*args, **kwargs)

    def set_full_name(self, name):
        parts = name.split(" ")
        if len(parts) < 1:
            return
        self.first_name = parts[0] if parts[0] else None
        last_name = " ".join(parts[1:])
        self.last_name = last_name if last_name.strip() else None

    def get_full_name(self):
        first = self.first_name or ""
        last = self.last_name or ""
        return f"{{first}} {{last}}".strip()

    name = property(get_full_name, set_full_name)
'''
        (users_dir / "models.py").write_text(models_content)

    def _create_env_example(self):
        content = f'''DJANGO_SECRET_KEY='{self._generate_secret_key()}'

DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME={self.project_name}
DB_USER={self.project_name}
DB_PASSWORD={self.project_name}
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/1
'''
        (self.src_dir / ".env.example").write_text(content)

    def _create_requirements_txt(self):
        lines = [f"{pkg}{ver}" for pkg, ver in self.BASE_PACKAGES]
        content = "\n".join(lines) + "\n"
        (self.base_dir / "requirements.txt").write_text(content)

    def _create_gitignore(self):
        content = '''__pycache__/
*.py[cod]
*$py.class
*.so
.env
.venv
venv/
ENV/
db.sqlite3
*.log
staticfiles/
media/
.DS_Store
.idea/
.vscode/
*.swp
*.swo
'''
        (self.base_dir / ".gitignore").write_text(content)