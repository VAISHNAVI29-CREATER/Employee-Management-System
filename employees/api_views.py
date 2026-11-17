
from django.db import transaction

from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)

from .models import Employee, Department, Project
from .serializers import (
    EmployeeSerializer,
    DepartmentSerializer,
    ProjectSerializer,
)
from .api_permissions import IsAdminOrEmployeeReadOnly, is_admin


class EmployeeViewSet(viewsets.ModelViewSet):
    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]

    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrEmployeeReadOnly]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "name",
        "employee_id",
        "email",
        "job_role",
    ]

    ordering_fields = [
        "name",
        "salary",
        "date_of_joining",
    ]

    ordering = ["id"]

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            queryset = Employee.objects.all()
        else:
            queryset = Employee.objects.filter(user=user)

        department = self.request.query_params.get("department")
        job_role = self.request.query_params.get("job_role")

        if department:
            queryset = queryset.filter(
                department_id=department
            )

        if job_role:
            queryset = queryset.filter(
                job_role__icontains=job_role
            )

        return queryset.select_related(
              "department",
              "user"
            ).prefetch_related(
               "projects"
            )

    # Database transaction for employee creation
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()

    # Database transaction for employee updates
    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()

    # Database transaction for employee deletion
    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.delete()


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by("id")
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrEmployeeReadOnly]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("id")
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrEmployeeReadOnly]


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        groups = list(
            user.groups.values_list("name", flat=True)
        )

        if user.is_superuser or "Admin" in groups:
            role = "Admin"
        elif "Employee" in groups:
            role = "Employee"
        else:
            role = "Unknown"

        return Response({
            "id": user.id,
            "username": user.username,
            "role": role,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })
