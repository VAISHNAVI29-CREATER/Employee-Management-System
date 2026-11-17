from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from .models import Employee, Department


class EmployeeAPITest(APITestCase):

    def setUp(self):
        self.department = Department.objects.create(
            name="IT",
            location="Coimbatore"
        )

        self.admin = User.objects.create_superuser(
            username="testadmin",
            email="admin@example.com",
            password="AdminPass123"
        )

        self.employee_group, _ = Group.objects.get_or_create(
            name="Employee"
        )

        self.employee_user = User.objects.create_user(
            username="testemployee",
            password="EmployeePass123"
        )

        self.employee_user.groups.add(self.employee_group)

        self.employee = Employee.objects.create(
            user=self.employee_user,
            employee_id="EMP001",
            name="Test Employee",
            email="employee@example.com",
            phone="9876543210",
            salary=Decimal("30000.00"),
            department=self.department,
            job_role="Python Developer",
            date_of_joining=date(2026, 1, 1)
        )

        self.list_url = reverse("employee-list")
        self.detail_url = reverse(
            "employee-detail",
            kwargs={"pk": self.employee.pk}
        )

        self.valid_payload = {
            "employee_id": "EMP002",
            "name": "New Employee",
            "email": "newemployee@example.com",
            "phone": "9876543211",
            "salary": "35000.00",
            "department": self.department.id,
            "job_role": "Software Developer",
            "date_of_joining": "2026-02-01",
            "projects": []
        }

    def test_admin_can_view_employees(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_employee(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Employee.objects.filter(employee_id="EMP002").exists()
        )

    def test_admin_can_update_employee(self):
        self.client.force_authenticate(user=self.admin)

        payload = {
            "employee_id": "EMP001",
            "name": "Updated Employee",
            "email": "employee@example.com",
            "phone": "9876543210",
            "salary": "40000.00",
            "department": self.department.id,
            "job_role": "Senior Developer",
            "date_of_joining": "2026-01-01",
            "projects": []
        }

        response = self.client.put(
            self.detail_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, "Updated Employee")

    def test_admin_can_partially_update_employee(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            self.detail_url,
            {"name": "Partially Updated"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, "Partially Updated")

    def test_admin_can_delete_employee(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Employee.objects.filter(pk=self.employee.pk).exists()
        )

    def test_employee_can_view_own_record(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_cannot_create_employee(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_update_employee(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.patch(
            self.detail_url,
            {"name": "Unauthorized Update"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_delete_employee(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_cannot_view_another_employee(self):
        another_employee = Employee.objects.create(
            employee_id="EMP003",
            name="Another Employee",
            email="another@example.com",
            phone="9876543212",
            salary=Decimal("32000.00"),
            department=self.department,
            job_role="Tester",
            date_of_joining=date(2026, 1, 5)
        )

        self.client.force_authenticate(user=self.employee_user)

        url = reverse(
            "employee-detail",
            kwargs={"pk": another_employee.pk}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_access_employees(self):
        response = self.client.get(self.list_url)

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )