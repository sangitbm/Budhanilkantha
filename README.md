# Budhanilkantha School Website

A modern Django-based school website with dynamic settings, custom models for staff, gallery, programs, and dynamic footer/hero customization.

## Setup Steps

1. Create a virtual environment:
   ```bash
   python -m venv myvenv
   ```
2. Activate the virtual environment:
   - Windows: `myvenv\\Scripts\\activate`
   - Linux/Mac: `source myvenv/bin/activate`
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your `SECRET_KEY`, `DEBUG`, etc.
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Seed default data (optional):
   ```bash
   python manage.py seed_programs
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Creating an Admin User
Run the following command to create a superuser for accessing the Django Admin panel:
```bash
python manage.py createsuperuser
```

## Running Tests
Run the test suite using Django's test runner:
```bash
python manage.py test
```

## Project Structure
- `config/` - Main Django settings, URL configurations, and WSGI/ASGI entry points.
- `core/` - The core application holding models like SiteSettings, AcademicProgram, Testimonial, as well as the main dashboard and public views.
- `news/` - News and notices application.
- `gallery/` - Image gallery application.
- `templates/` - Global HTML templates.
- `static/` - Static files (CSS, JS, images).
- `media/` - User-uploaded media files (ignored in version control).
