
# Artlysoft Day 6 – Employee Management System

## Objective
To develop a basic Employee Management web application using Django, demonstrating MVT architecture, URL routing, views, templates, and the request–response lifecycle.

## Features
- Home page with employee management information
- Employee directory with sample employee details
- Navigation links between pages
- Django views and URL routing
- HTML templates with responsive styling

## Technologies
- Python
- Django
- HTML and CSS
- Virtual environment (`venv`)

## Setup and Execution

1. Open a terminal and navigate to the project folder.
2. Create and activate a virtual environment if one does not already exist:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Apply Django migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Open these addresses in a browser:

   - Home: http://127.0.0.1:8000/
   - Employees: http://127.0.0.1:8000/employees/

## MVT Architecture
- Model: Represents and manages application data.
- View: Processes requests and returns responses.
- Template: Defines the HTML presentation.

## Request–Response Lifecycle
The browser sends a request. Django resolves its URL, calls the corresponding view, renders a template, and returns an HTTP response.

## Project Structure
- `manage.py`: Django management commands
- `config/settings.py`: Project configuration
- `config/urls.py`: Main URL configuration
- `employees/views.py`: Page logic
- `employees/urls.py`: App URL routes
- `employees/templates/employees/`: HTML templates
- `requirements.txt`: Python dependencies

## Limitations
The employee details are sample data stored in the view. Database-backed employee records and CRUD operations are outside the scope of this basic assignment.

## Conclusion
The project demonstrates the fundamentals of Django and provides a foundation for building more advanced employee management applications.

# Employee Management System

## Project Overview
The Employee Management System is a full-stack web application developed using Django REST Framework, React, and MariaDB.

It allows administrators to manage employee records and employees to securely view their own profile information.

## Technologies Used

### Backend
- Python
- Django
- Django REST Framework
- MariaDB
- Token Authentication

### Frontend
- React
- Vite
- React Router
- Axios
- Bootstrap 5

## Main Features

### Admin
- Admin login and logout
- View all employee records
- Add new employees
- Edit employee information
- Delete employee records
- View departments and projects

### Employee
- Employee login and logout
- View personal employee details
- Restricted access to other employees' records
- Cannot perform employee CRUD operations

### Security
- Token-based authentication
- Protected routes
- Role-based access control
- API permission validation

### Responsive Design
- Desktop dashboard
- Mobile-friendly dashboard
- Responsive employee forms and tables

## Project Structure

```text
Artlysoft-Day6/
├── config/
├── employees/
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── routes/
│   │   └── services/
│   └── package.json
├── screenshots/
│   ├── Day14/
│   └── Day15/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Backend Setup

```bash
cd ~/Artlysoft-Day6
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure the following environment variables using your own values:

- DB_PASSWORD
- DJANGO_SECRET_KEY

### 2. Run Django Backend

```bash
python manage.py migrate
python manage.py runserver
```

Backend URL: http://127.0.0.1:8000/

### 3. Frontend Setup

Open another terminal:

```bash
cd ~/Artlysoft-Day6/frontend
pnpm install
pnpm dev
```

Open the local URL displayed by Vite.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/auth/token/ | Login |
| GET | /api/auth/user/ | Current user details |
| GET | /api/employees/ | List employees |
| POST | /api/employees/ | Add employee |
| PATCH | /api/employees/{id}/ | Update employee |
| DELETE | /api/employees/{id}/ | Delete employee |
| GET | /api/departments/ | List departments |
| GET | /api/projects/ | List projects |

## Testing

The following functionality was tested:

- Admin authentication
- Employee authentication
- Employee CRUD operations
- Role-based access restrictions
- Protected routes
- Employee profile display
- Responsive desktop and mobile layouts
- Frontend production build

## Screenshots

Project screenshots are available in:

- screenshots/Day14/
- screenshots/Day15/

## Developer

Developed as part of the Artlysoft Python Full-Stack Development Internship Program.
## Day 18 – Testing, Debugging and Security

### Automated Testing

Django testing was implemented using Django TestCase and Django REST Framework APITestCase.

**Django Model Tests**
- Department creation and string representation.
- Project creation and string representation.
- Employee creation and relationships.
- Employee and project relationships.

**Django API Tests**
- Admin GET, POST, PUT, PATCH and DELETE operations.
- Employee read-only access.
- Employee access restricted to their own records.
- Unauthorized employee CRUD operations.
- Unauthenticated API access restrictions.

**FastAPI Tests**

Automated testing was implemented using Pytest and FastAPI TestClient.

- GET all employees.
- GET employee by ID.
- POST employee creation.
- PUT employee updates.
- DELETE employee records.
- Search and department filtering.
- Duplicate employee ID validation.
- Invalid employee data validation.
- 404 error handling.
- Asynchronous endpoint testing.

### Test Results

| Project | Tests Passed |
|---|---:|
| Django Model Tests | 9/9 |
| Django API Tests | 11/11 |
| FastAPI Tests | 13/13 |
| **Total** | **33/33** |

### Environment Variable Configuration

Sensitive configuration values are stored in a local `.env` file.

Environment variables:
- DJANGO_SECRET_KEY
- DB_PASSWORD

The `python-dotenv` package loads environment variables into Django settings.

A `.env.example` file provides sample configuration without exposing actual credentials.

### Security

- `.env` is excluded through `.gitignore`.
- `.env.example` is included as a safe configuration template.
- Private environment file permissions are restricted.
- Role-based API permissions protect employee records.
- Admin and Employee access restrictions are tested.

### Application Logging

Django logging is configured to record application events and request information.

Log file: `logs/django.log`

Logging includes timestamps, log levels, logger names and messages.

### Testing Commands

**Django:**

```bash
python manage.py check
python manage.py test employees
```

**FastAPI:**

```bash
python -m pytest -v
```

### Conclusion

Day 18 demonstrates automated testing, CRUD validation, authentication and permission testing, error handling, application logging and secure environment configuration across Django REST Framework and FastAPI.