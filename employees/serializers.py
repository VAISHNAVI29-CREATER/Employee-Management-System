
from rest_framework import serializers
from .models import Employee, Department, Project
from decimal import Decimal


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):

    department_name = serializers.CharField(
        source="department.name",
        read_only=True
    )

    project_names = serializers.StringRelatedField(
        source="projects",
        many=True,
        read_only=True
    )

    salary = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
        required=True
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "name",
            "email",
            "phone",
            "salary",
            "department",
            "department_name",
            "job_role",
            "date_of_joining",
            "projects",
            "project_names",
            "profile_image",
        ]

    def validate_employee_id(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Employee ID cannot be empty."
            )
        return value

    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )
        return value

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Salary must be greater than zero."
            )
        return value

    def validate_profile_image(self, value):
        if value:
            allowed_types = [
                "image/jpeg",
                "image/png",
                "image/webp",
            ]

            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Only JPEG, PNG and WebP images are allowed."
                )

            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError(
                    "Image size must not exceed 2 MB."
                )

        return value
