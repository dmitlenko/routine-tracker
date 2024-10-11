# Routine Tracker


## Functionality Requirements
1. User can create routine groups (for example 'Guitar practicing', 'Piano mastering')
    - User can input name, description, icon, and color for the routine group
    - User can add routines to the group
2. Every routine should contain relevant data such as name, description, etc.
    - User can select type of the routine value: check (box), number, date, time
    - User can input name, description, icon, and color for the routine
3. App should show statistics based on user data
    - Single routine chart
    - Routine group chart
    - Some message to user like ('You are getting better at X' or 'Your performance is N% higher compared to the last M days')
4. User can set up reminders for routines
    - User can set up time and days for reminders
5. Other
    - User can export routine data in popular formats (CSV, JSON)
    - App should support multiple languages or at least English and Ukrainian


## Technical Requirements

### General
1. App should implement all functionality requirements
2. App should be deployable with Docker

### Backend
1. Backend should be built with Django
2. Database should be PostgreSQL

### Frontend
1. Frontend will be driven by Django templates
2. Frontend should be written in HTML, CSS, and JavaScript (HTMX)
3. App should have a user-friendly interface
4. App should have a dark mode


## Technologies

### Backend
- Python
- [Django](https://docs.djangoproject.com/en/5.1/)
- [PostgreSQL via Django](https://docs.djangoproject.com/en/5.1/ref/databases/#postgresql-notes)
- [django-htmx](https://django-htmx.readthedocs.io/en/latest/)

### Frontend
- [HTMX](https://htmx.org/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.1/getting-started/introduction/)

### Deployment
- [Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Development

#### General
- [VS Code](https://code.visualstudio.com/)
- [EditorConfig (for consistent coding styles)](https://editorconfig.org/)
- [Make (for running commands)](https://www.gnu.org/software/make/)
- [Git (for version control)](https://git-scm.com/)
- [pre-commit (for running checks before commit)](https://pre-commit.com/)

#### Backend
- [Poetry (for Python dependencies)](https://python-poetry.org/)
- [flake8 (for linting)](https://flake8.pycqa.org/en/latest/)
- [Black (for formatting)](https://black.readthedocs.io/en/stable/)
