# Django Simple Starter

Django Simple Starter (`dss`) is a CLI tool to quickly scaffold Django projects with your preferred setup.

## Quick Start

```bash
pip install django-simple-starter
dss myproject
```

## What it creates

- Django project with settings module (common, development, preprod, production)
- Custom User model with UserManager
- BaseModel with UUID primary key
- env.example and requirements.txt
- .gitignore

## Default Packages

- Django>=5.2,<6.0
- djangorestframework>=3.17
- django-cors-headers>=4.9
- python-decouple>=3.8
- psycopg2-binary>=2.9
- django-phonenumber-field>=8.4
- Pillow>=11
- django-redis>=5.0

## Usage

```bash
# Create a new project
dss myproject
cd myproject

# Copy env file and set up
cp src/.env.example src/.env

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python src/manage.py migrate

# Run server
python src/manage.py runserver
```

## Development

```bash
# Install locally
pip install -e .

# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## License

MIT