# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# Day 14 – Employee Management System

## Project Overview
A full-stack Employee Management System developed using Django REST Framework and React. The application connects the React frontend to Django REST APIs using Axios.

## Technologies Used
- Backend: Python, Django, Django REST Framework
- Frontend: React, Vite, JavaScript
- API Communication: Axios
- Database: MariaDB
- Authentication: Token Authentication
- Styling: CSS

## Features
- User login and logout
- Token-based authentication
- View employee records
- Add new employees
- Update employee details
- Delete employee records
- Department dropdown
- Project selection
- Form validation
- Loading indicators
- API error handling
- Success messages
- Role-based permissions

## API Endpoints

| Method | Endpoint | Operation |
|---|---|---|
| GET | /api/employees/ | List employees |
| POST | /api/employees/ | Create employee |
| GET | /api/employees/{id}/ | View employee |
| PATCH | /api/employees/{id}/ | Update employee |
| DELETE | /api/employees/{id}/ | Delete employee |
| GET | /api/departments/ | List departments |
| GET | /api/projects/ | List projects |
| POST | /api/auth/token/ | Authentication |

## Installation and Execution

### Backend

1. Navigate to the project directory.
2. Activate the virtual environment:

```bash
source .venv/bin/activate
```

3. Configure the required environment variables:

```bash
export DB_PASSWORD='YOUR_DATABASE_PASSWORD'
export DJANGO_SECRET_KEY='YOUR_DJANGO_SECRET_KEY'
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Start the Django server:

```bash
python manage.py runserver
```

Backend URL: http://127.0.0.1:8000/

### Frontend

Open another terminal:

```bash
cd frontend
pnpm install
pnpm dev
```

Frontend URL: http://localhost:5173/

If Vite selects another available port, use the URL shown in the terminal.

## Access Permissions

**Admin**
- View all employee records
- Create employees
- Update employees
- Delete employees

**Employee**
- View their own employee record
- Cannot create, update or delete employee records

## Testing
The following operations were tested:
- Authentication
- Employee listing
- Employee creation
- Employee updating
- Employee deletion
- Employee permission restrictions

## Screenshots
Screenshots are available in `screenshots/Day14/`.

## Conclusion
The React frontend was successfully integrated with the Django REST API using Axios. Employee CRUD operations, authentication, validation and role-based access control were tested.