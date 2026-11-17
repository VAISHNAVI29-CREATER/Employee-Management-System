
from django.conf import settings
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    profile_image = models.ImageField(
        upload_to="employee_profiles/",
        blank=True,
        null=True
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile"
    )

    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees"
    )

    job_role = models.CharField(max_length=100, db_index=True)
    date_of_joining = models.DateField()

    projects = models.ManyToManyField(
        Project,
        blank=True,
        related_name="employees"
    )

    def __str__(self):
        return f"{self.employee_id} - {self.name}"
