from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Department, Project, Employee


class DepartmentModelTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(
            name="Information Technology",
            location="Coimbatore"
        )

    def test_department_creation(self):
        self.assertEqual(self.department.name, "Information Technology")
        self.assertEqual(self.department.location, "Coimbatore")

    def test_department_string_representation(self):
        self.assertEqual(str(self.department), "Information Technology")


class ProjectModelTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            name="Employee Management System",
            description="Django project",
            start_date=date(2026, 1, 1)
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Employee Management System")

    def test_project_string_representation(self):
        self.assertEqual(str(self.project), "Employee Management System")


class EmployeeModelTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(
            name="IT",
            location="Coimbatore"
        )

        self.user = User.objects.create_user(
            username="testemployee",
            password="testpassword123"
        )

        self.employee = Employee.objects.create(
            user=self.user,
            employee_id="TEST001",
            name="Test Employee",
            email="test@example.com",
            phone="9876543210",
            salary=Decimal("30000.00"),
            department=self.department,
            job_role="Python Developer",
            date_of_joining=date(2026, 1, 1)
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.name, "Test Employee")
        self.assertEqual(self.employee.salary, Decimal("30000.00"))

    def test_employee_string_representation(self):
        self.assertEqual(
            str(self.employee),
            "TEST001 - Test Employee"
        )

    def test_employee_department_relationship(self):
        self.assertEqual(self.employee.department.name, "IT")

    def test_employee_user_relationship(self):
        self.assertEqual(self.employee.user.username, "testemployee")

    def test_employee_project_relationship(self):
        project = Project.objects.create(name="Testing Project")
        self.employee.projects.add(project)

        self.assertIn(project, self.employee.projects.all())